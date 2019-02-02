#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-01-30 18:17
# @Author  : pang
# @File    : nav_spider.py
# @Software: PyCharm

# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-01-30 11:20
# @Author  : pang
# @File    : fund_spider.py
# @Software: PyCharm

import logging
import os

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
        'RETRIES': 0,
        'DELAY': 1,
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
        self.fund_codes = None

    async def get_fund_codes(self):
        cursor = self.client[self.db_name][self.id_map_collection].find()
        async for doc in cursor:
            yield doc['jfz_id']

    async def start_requests(self):
        async for jfz_id in self.get_fund_codes():
            url = "https://www.jfz.com/simu/chart?id=%s" % jfz_id
            yield self.make_requests_from_url(url=url)
            break

    async def parse(self, response: Response):
        try:
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
