#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-01-30 18:17
# @Author  : pang
# @File    : nav_spider.py
# @Software: PyCharm

import os
import asyncio
import logging
import datetime

from motor.motor_asyncio import AsyncIOMotorClient

from ruia import Spider, Response

try:
    from items import FundItem
except ImportError:
    import sys
    sys.path[0] = os.path.dirname(os.path.abspath(__file__))
    from items import FundItem

MONGODB_URL = os.environ.get('MONGODB_URL')
if not MONGODB_URL:
    MONGODB_URL = "mongodb://192.168.1.251:27017"
DB_NAME = "privately_fund"


class NavSpider(Spider):
    request_config = {
        'RETRIES': 2,
        'DELAY': 5,
        'TIMEOUT': 20
    }
    concurrency = 2

    kwargs = {}
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive',
               'Host': 'www.jfz.com', 'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'}

    def __init__(self, middleware=None, loop=None, is_async_start=False):
        super().__init__(middleware, loop, is_async_start)
        self.client = AsyncIOMotorClient(MONGODB_URL, io_loop=loop)
        self.db_name = DB_NAME
        self.collection = 'jfz:nav'
        self.id_map_collection = 'fund_id_map'
        self.fund_codes = None

    async def get_fund_codes(self):
        cursor = self.client[self.db_name][self.id_map_collection].find()
        async for doc in cursor:
            yield doc['_id'], doc['jfz_id']
            # break

    async def start_requests(self):
        async for _id, jfz_id in self.get_fund_codes():
            url = "https://www.jfz.com/simu/chart?id=%s" % jfz_id
            metadata = {'_id': _id}
            yield self.make_requests_from_url(url=url, res_type='json', metadata=metadata)

    async def parse(self, response: Response):
        try:
            data = response.html
            if data is None or len(data) != 2:
                logging.info("采集失败. url:%s" % response.url)
                return
            data = data[0]['data']
            _id = response.metadata['_id']
            update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            tasks = []
            for item in data:
                ts = float(item['x']) / 1000.0
                sum_nav = float(item['y'])
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y%m%d")
                row = {'sum_nav': sum_nav, 'update_time': update_time}
                co = self.client[self.db_name][self.collection].update_one({'fund_id': _id, 'date': date}, {'$set': row}, upsert=True)
                task = asyncio.ensure_future(co, loop=self.loop)
                tasks.append(task)
            await asyncio.gather(*tasks)
            return
        except Exception as e:
            logging.exception(e)
            return


"""
累计净值接口:
https://www.jfz.com/simu/chart?id=P6281mbsw2
所有净值接口(需要登录):
https://www.jfz.com/simu/simuProductNew/GetPrdNetWorthDrawDown?prdCode=P6281mbsw2

"""

if __name__ == '__main__':
    NavSpider.start()
