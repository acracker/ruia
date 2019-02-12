#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-01-17 13:49
# @Author  : pang
# @File    : fund.py
# @Software: PyCharm

import datetime
import os
import asyncio
import re
import logging
import time
import random

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

# http://gs.amac.org.cn/amac-infodisc/api/pof/fund?rand=0.03935877331629101&page=0&size=20


class FundSpider(Spider):
    request_config = {
        'RETRIES': 0,
        'DELAY': 1,
        'TIMEOUT': 20
    }
    name = 'full_spider'
    concurrency = 10
    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive', 'Content-Length': '2', 'Content-Type': 'application/json', 'Host': 'gs.amac.org.cn',
               'Origin': 'http://gs.amac.org.cn', 'Referer': 'http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'}

    def __init__(self, middleware=None, loop=None, is_async_start=False):
        super().__init__(middleware, loop, is_async_start)
        self.client = AsyncIOMotorClient(MONGODB_URL, io_loop=loop)
        self.db_name = DB_NAME
        self.fund_collection = self.client[self.db_name]['fund']

    async def get_total_pages(self):
        url = "http://gs.amac.org.cn/amac-infodisc/api/pof/fund?rand={rand}&page=0&size=20".format(rand=random.random())
        request = self.make_requests_from_url(url, data=b"{}", method="POST", res_type='json')
        resp = await request.fetch()
        if resp.status == 200:
            if 'totalPages' in resp.html:
                return resp.html['totalPages']
        raise ValueError('failed to get total pages.')

    async def start_requests(self):
        num = await self.get_total_pages()
        for i in range(num):
            url = "http://gs.amac.org.cn/amac-infodisc/api/pof/fund?rand={rand}&page={page}&size=20".format(rand=random.random(), page=i)
            yield self.make_requests_from_url(url, data=b"{}", method="POST", res_type='json')

    async def parse(self, response: Response):
        data = response.html
        if data is None or 'content' not in data:
            return None
        data = data['content']
        update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for item in data:
            row = dict()
            row['register_number'] = item['fundNo']
            row['full_name'] = str(item['fundName']).replace(' ', '')
            row['company_name'] = item['managerName']
            row['manager_type'] = item['managerType']
            row['status'] = item['workingState']
            try:
                row['establish_date'] = datetime.datetime.fromtimestamp(item['establishDate'] / 1000).strftime("%Y%m%d")
            except:
                row['establish_date'] = item['establishDate']
            row['company_url'] = item['managerUrl']
            row['mandator_name'] = item['mandatorName']
            row['last_quarter_update'] = item['lastQuarterUpdate']
            row['is_depute_manage'] = item['isDeputeManage']
            try:
                row['put_on_record_date'] = datetime.datetime.fromtimestamp(item['putOnRecordDate'] / 1000).strftime("%Y%m%d")
            except:
                row['put_on_record_date'] = item['putOnRecordDate']
            row['update_time'] = update_time
            s = time.time()
            await self.fund_collection.update_one({'register_number': row['register_number'], 'full_name': row['full_name']}, {'$set': row}, upsert=True)
            e = time.time()
            self.logger.info("采集基金[%s]信息,  存储耗时:%s s" % (row['register_number'], round(e - s, 2)))


if __name__ == '__main__':
    FundSpider.start()
