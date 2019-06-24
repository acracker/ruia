#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-02-11 11:22
# @Author  : pang
# @File    : fund_info_spider.py
# @Software: PyCharm
import datetime
import os
import asyncio
import re
import logging
import time

import aiohttp
from motor.motor_asyncio import AsyncIOMotorClient
from ruia import Request, Spider, Response

try:
    from items import FundInfoItemV1
    from settings import *
except ImportError:
    import sys
    sys.path[0] = os.path.dirname(os.path.abspath(__file__))
    from items import FundInfoItemV1
    from settings import *


"""
根据基金排行中找到的编号 爬取 基金信息页面

https://www.jfz.com/simu/p-P6281mbsw2.html

"""


class FundInfoSpider(Spider):
    request_config = {
        'RETRIES': 0,
        'DELAY': 2,
        'TIMEOUT': 20
    }
    name = 'full_info_spider'
    concurrency = 3
    kwargs = {
        'proxy': HTTP_PROXY,
    }

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive',
               'Host': 'www.jfz.com', 'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'}

    def __init__(self, middleware=None, loop=None, is_async_start=False):
        super().__init__(middleware, loop, is_async_start)
        self.logger.info('MONGODB_URL:%s' % MONGODB_URL)
        self.client = AsyncIOMotorClient(MONGODB_URL, io_loop=loop)
        self.db_name = DB_NAME
        self.fund_info_collection = self.client[self.db_name]['%s:fund' % SOURCE]
        self.request_session = None
        self.sem = asyncio.Semaphore(self.concurrency, loop=self.loop)

    async def get_all_fund(self):
        try:
            limit = int(os.environ.get('LIMIT', 0))
            self.logger.info("LIMIT:%s" % limit)
        except ValueError:
            limit = 0
        cursor = self.fund_info_collection.find(limit=limit)
        cursor.sort('update_time', 1)
        count = 0
        async for doc in cursor:
            yield doc
            count += 1

    async def start_requests(self):
        self.request_session = aiohttp.ClientSession()
        now_time = datetime.datetime.now()
        async for doc in self.get_all_fund():
            jfz_id = doc['id']
            if 'update_time' in doc.keys():
                str_update_time = doc['update_time']
                update_time = datetime.datetime.strptime(str_update_time, '%Y-%m-%d %H:%M:%S')
                if (now_time - update_time).days <= 3:
                    # 如果当天天内采集过的, 则跳过
                    self.logger.debug("最近更新过,跳过. ID: %s, 上次更新时间:%s" % (jfz_id, str_update_time))
                    continue
            url = 'https://www.jfz.com/simu/p-%s.html' % jfz_id
            meta = {'jfz_id': jfz_id}
            yield self.make_requests_from_url(url=url, meta=meta)
            self.logger.info("生成采集请求. ID:%s" % jfz_id)

    async def parse(self, response: Response):
        try:
            update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if response.html is None:
                self.logger.warning("网页解析错误. url:%s" % response.url)
                return
            data = await FundInfoItemV1.get_item(html=response.html)
            product_info = data.product_info
            if product_info is None:
                self.logger.warning("网页解析错误. url:%s" % response.url)
            jfz_id = response.meta['jfz_id']
            register_number = product_info['register_number']
            full_name = product_info['full_name']
            establishment_date = product_info['build_date']
            row = {
                'register_number': register_number,
                'full_name': full_name,
                'establish_date': establishment_date,
                'update_time': update_time,
                'id': jfz_id,
            }
            s = time.time()
            await self.fund_info_collection.update_one({'id': jfz_id}, {'$set': row}, upsert=True)
            e = time.time()
            self.logger.info("采集基金[%s]产品信息,  存储耗时:%s s" % (jfz_id, round(e - s, 2)))
        except Exception as e:
            self.logger.warning("网页解析错误. url:%s" % response.url)
            logging.exception(e)
            return


async def before_stop(spider):
    if spider.request_session:
        await spider.request_session.close()


if __name__ == '__main__':
    FundInfoSpider.start(before_stop=before_stop)
