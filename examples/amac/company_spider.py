#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-01-16 16:42
# @Author  : pang
# @File    : company_spider.py
# @Software: PyCharm
import datetime
import os
import asyncio
import re
import logging
import time
import random

import aiohttp
from collections import OrderedDict
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
从协会网站抓取所有投顾的基本信息, 不包括扩展信息
更新间隔可以略长
"""

url_search_manager = r'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.258368130618152&page=0&size=20'
headers_search_company = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Referer': 'http//gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

url_company_detail = r"http://gs.amac.org.cn/amac-infodisc/res/pof/manager/{company_id}.html"
headers_company_detail = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                          'Accept-Encoding': 'gzip, deflate',
                          'Accept-Language': 'zh-CN,zh;q=0.9',
                          'Cache-Control': 'no-cache',
                          'Connection': 'keep-alive',
                          'Cookie': 'look=first',
                          'Host': 'gs.amac.org.cn',
                          'Pragma': 'no-cache',
                          'Upgrade-Insecure-Requests': '1',
                          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'}


class CompanySpider(Spider):
    request_config = {
        'RETRIES': 1,
        'DELAY': 3,
        'TIMEOUT': 20
    }
    concurrency = 3
    name = 'company_spider'
    kwargs = {
        'proxy': HTTP_PROXY,
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Referer': 'http//gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    def __init__(self, middleware=None, loop=None, is_async_start=False):
        super().__init__(middleware, loop, is_async_start)
        self.client = AsyncIOMotorClient(MONGODB_URL, io_loop=loop)
        self.db_name = DB_NAME
        self.fund_collection = self.client[self.db_name]['company']

    async def start_requests(self):
        num = await self.get_total_pages()
        for i in range(num):
            url = "http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand={rand}&page={page}&size=20".format(rand=random.random(), page=i)
            yield self.make_requests_from_url(url, data=b"{}", method="POST", res_type='json')

    async def get_total_pages(self):
        url = "http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand={rand}&page=0&size=20".format(rand=random.random())
        request = self.make_requests_from_url(url, data=b"{}", method="POST", res_type='json')
        resp = await request.fetch()
        if resp.status == 200:
            if 'totalPages' in resp.html:
                return resp.html['totalPages']
        raise ValueError('failed to get total pages.')

    async def parse(self, response: Response):
        data = response.html
        if data is None or 'content' not in data:
            self.logger.info("采集失败. url:%s" % response.url)
            return None
        try:
            data = data['content']
            tasks = []
            update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            for item in data:
                row = dict()
                row['company_name'] = str(item['managerName']).replace(' ', '')
                row['artificial_person_name'] = item['artificialPersonName']
                row['register_number'] = item['registerNo']
                try:
                    row['establish_date'] = datetime.datetime.fromtimestamp(item['establishDate'] / 1000).strftime("%Y%m%d")
                except:
                    row['establish_date'] = item['establishDate']
                row['manager_has_product'] = item['managerHasProduct']
                row['url'] = item['url']
                try:
                    row['register_date'] = datetime.datetime.fromtimestamp(item['registerDate'] / 1000).strftime("%Y%m%d")
                except:
                    row['register_date'] = item['registerDate']
                row['register_address'] = item['registerAddress']
                row['register_province'] = item['registerProvince']
                row['register_city'] = item['registerCity']
                row['reg_ddr_agg'] = item['regAdrAgg']
                row['fund_count'] = item['fundCount']
                row['fund_scale'] = item['fundScale']
                row['paid_in_capital'] = item['paidInCapital']
                row['subscribed_capital'] = item['subscribedCapital']
                row['has_special_tips'] = item['hasSpecialTips']
                row['in_black_list'] = item['inBlacklist']
                row['has_credit_tips'] = item['hasCreditTips']
                row['reg_coordinate'] = item['regCoordinate']
                row['office_coordinate'] = item['officeCoordinate']
                row['office_address'] = item['officeAddress']
                row['office_province'] = item['officeProvince']
                row['office_city'] = item['officeCity']
                row['primary_investType'] = item['primaryInvestType']
                row['update_time'] = update_time
                co = self.fund_collection.update_one({'register_number': row['register_number'], 'company_name': row['company_name']}, {'$set': row},
                                                     upsert=True)
                tasks.append(asyncio.ensure_future(co, loop=self.loop))
            s = time.time()
            await asyncio.gather(*tasks)
            e = time.time()
            self.logger.info("采集%s条投顾信息,  存储耗时:%s s" % (len(data), round(e - s, 2)))
        except Exception as e:
            self.logger.info("采集失败. url:%s" % response.url)
            self.logger.exception(e)
            await self.stop()

        # title = response.html_etree.xpath('//td[@class="td-title"]')
        # content = response.html_etree.xpath('//td[@class="td-content"]')
        # result = OrderedDict()
        # company_code = response.meta['company_code']
        # for k, v in zip(title, content):
        #     result[k.text] = v
        # company_name = result['基金管理人全称(中文):'].xpath('//div[@id="complaint1"]')[0].text
        # # company_name = re.sub('')
        # company_name = re.sub(r'&[a-z]{4}', '', company_name)
        # company_name = re.sub(r'\s', '', company_name)
        # qualification = result['是否为符合提供投资建议条件的第三方机构:'].text
        # async with lock:
        #     _result[company_code] = (company_name, qualification)
        # return None

    async def search_company(self, keyword="平安道远投资管"):
        # 请输入登记编号/私募基金管理人名称或法定代表人/执行事务合伙人（委派代表）姓名
        body = {"keyword": keyword}
        request = self.make_requests_from_url(url=url_search_manager, method='POST', headers=headers_search_company, json=body, res_type='json')
        response = await request.fetch()
        data = response.html
        result = []
        pattern = r'<.*?>'
        if 'content' in data and len(data['content']) != 0:
            for item in data['content']:
                for k, v in item.items():
                    if isinstance(v, str):
                        v = re.sub(pattern, '', v)
                        item[k] = v
                result.append(item)
        else:
            logging.warning("投顾搜索失败. keyword:%s" % keyword)
        return result

    async def crawl_company_detail(self, company_id="101000000138"):
        request = self.make_requests_from_url(url=url_company_detail.format(company_id=company_id), headers=headers_company_detail)
        response = await request.fetch()
        title = response.html_etree.xpath('//td[@class="td-title"]')
        content = response.html_etree.xpath('//td[@class="td-content"]')
        result = OrderedDict()
        for k, v in zip(title, content):
            result[k.text] = v.text
        return result


if __name__ == '__main__':
    CompanySpider.start()
