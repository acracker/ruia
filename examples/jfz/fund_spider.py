#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-01-30 11:20
# @Author  : pang
# @File    : fund_spider.py
# @Software: PyCharm
import os
import asyncio
import re
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from ruia import Request, Spider, Response

try:
    from items import FundItem
except ImportError:
    import os
    import sys
    sys.path[0] = os.path.dirname(os.path.abspath(__file__))
    from items import FundItem

MONGODB_URL = os.environ.get('MONGODB_URL')
if not MONGODB_URL:
    MONGODB_URL = "mongodb://192.168.1.251:27017"
DB_NAME = "privately_fund"


"""
从金斧子 私募排行页面中 抓取所有基金的基础信息, 编号, 策略信息, 投顾信息.

"""


class FundSpider(Spider):
    request_config = {
        'RETRIES': 0,
        'DELAY': 2,
        'TIMEOUT': 20
    }
    # concurrency = 3

    kwargs = {}
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive',
               'Host': 'www.jfz.com', 'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'}

    def __init__(self, middleware=None, loop=None, is_async_start=False):
        super().__init__(middleware, loop, is_async_start)
        self.client = AsyncIOMotorClient(MONGODB_URL, io_loop=loop)
        self.db_name = DB_NAME
        self.collection = 'jfz:fund'
        self.id_map_collection = 'fund_id_map'

    async def get_total_pages(self):
        # request = self.make_requests_from_url("https://www.jfz.com/simu/list_w1_r1_p1.html")
        request = self.make_requests_from_url("https://www.jfz.com/simu/list_w1_r1.html")
        resp = await request.fetch()
        if resp.status == 200:
            elements = resp.html_etree.xpath('//li[@class="page-item page-last"]/a/@href')
            if len(elements) == 1:
                pate_last_url = str(elements[0])
                match = re.match(r'.*?p(\d+)\.htm', pate_last_url)
                if match:
                    return int(match.group(1))
        raise ValueError('failed to get total pages.')

    async def start_requests(self):
        num = await self.get_total_pages()
        # num = 1
        for i in range(1, num+1):
            url = "https://www.jfz.com/simu/list_w1_r1_p%s.html" % i
            yield self.make_requests_from_url(url=url)

    async def parse(self, response: Response):
        try:
            items = await FundItem.get_item(html=response.html)
            tasks = []
            for row in items.rows:
                logging.debug("item:%s" % str(row))
                co = self.client[self.db_name][self.collection].update_one({'id': row['id']}, {'$set': row}, upsert=True)
                task = asyncio.ensure_future(co, loop=self.loop)
                tasks.append(task)
                co = self.client[self.db_name][self.id_map_collection].update_one({'jfz_id': row['id']}, {'$set': {'jfz_id': row['id']}}, upsert=True)
                task = asyncio.ensure_future(co, loop=self.loop)
                tasks.append(task)
            await asyncio.gather(*tasks)
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
    FundSpider.start()
