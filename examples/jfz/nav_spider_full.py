#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-01-30 18:17
# @Author  : pang
# @Software: PyCharm
import re
import os
import time
import asyncio
import datetime
import aiohttp
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import UpdateOne

from ruia import Spider, Response

try:
    from items import FundItem
    from settings import *
except ImportError:
    import sys
    sys.path[0] = os.path.dirname(os.path.abspath(__file__))
    from items import FundItem
    from settings import *


def make_task_persist_update_detail(_id, source='jfz', update_time=None):
    """
    插入净值更新时间, 方便查询爬取净值
    :param _id:
    :param source:
    :param update_time:
    :return:
    """
    update_time = update_time or datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return UpdateOne({'%s_id' % source: _id}, {'$set': {'%s_update_time' % source: update_time}}, upsert=True)


class NavSpider(Spider):
    request_config = {
        'RETRIES': 0,
        'DELAY': 5,
        'TIMEOUT': 20
    }
    concurrency = 3
    name = 'full_nav_spider'
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
        self.nav_collection = self.client[self.db_name]['%s:nav' % SOURCE]
        self.id_map_collection = self.client[self.db_name]['fund_id_map']
        self.token = None
        self.request_session = None
        self.sem = asyncio.Semaphore(self.concurrency, loop=self.loop)

    async def login(self):
        url = "https://passport.jinfuzi.com/passport/user/loginAjax?cb=" \
              "jQuery1102013622709964876956_1533719058287&LoginForm%5Busername%5D=13608228554" \
              "&LoginForm%5Bpassword%5D=z123456&_=1533719058293"
        request = self.make_requests_from_url(url=url)
        resp = await request.fetch()
        if resp.status != 200:
            return False
        text = resp.html
        pattern = r'.*?\(\[(\d+),.*"authToken":"(.*?)"\}\]\)'
        m = re.match(pattern, text)
        if not m:
            return False
        if m.group(1) != '10000':
            return False
        self.token = m.group(2)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'Host': 'www.jfz.com',
        }
        url = "https://www.jfz.com/public/login/index?authToken=%s" % self.token
        request = self.make_requests_from_url(url=url, headers=headers)
        resp = await request.fetch()
        result = resp.status == 200
        if not result:
            return False
        return True

    async def get_all_fund(self):
        try:
            limit = int(os.environ.get('LIMIT', 0))
            limit = 0
            print("test")       # todo
            self.logger.info("LIMIT:%s" % limit)
        except ValueError:
            limit = 0
        cursor = self.id_map_collection.find(limit=limit)
        cursor.sort('%s_update_time' % SOURCE, 1)
        # cursor = self.client[self.db_name][self.id_map_collection].find()
        count = 0
        async for doc in cursor:
            yield doc
            count += 1
            # break

    async def start_requests(self):
        self.request_session = aiohttp.ClientSession()
        if await self.login():
            self.logger.info("登录成功")
        else:
            self.logger.warning("登录失败")
            return
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'Host': 'www.jfz.com',
        }
        now_time = datetime.datetime.now()
        async for doc in self.get_all_fund():
            if '%s_id' % SOURCE not in doc.keys():
                continue
            _id, jfz_id = doc['_id'], doc['%s_id' % SOURCE]
            if '%s_update_time' % SOURCE in doc.keys():
                str_update_time = doc['%s_update_time' % SOURCE]
                update_time = datetime.datetime.strptime(str_update_time, '%Y-%m-%d %H:%M:%S')
                if (now_time - update_time).days <= 1:
                    # 如果当天天内采集过的, 则跳过
                    self.logger.debug("最近更新过,跳过. ID: %s, 上次更新时间:%s" % (jfz_id, str_update_time))
                    continue
            url = 'https://www.jfz.com/simu/simuProductNew/GetPrdNetWorthDrawDown?prdCode=%s' % jfz_id
            # url = "https://www.jfz.com/simu/chart?id=%s" % jfz_id
            metadata = {'_id': _id, 'jfz_id': jfz_id}
            yield self.make_requests_from_url(url=url, res_type='json', metadata=metadata, headers=headers)
            self.logger.info("生成采集请求. ID:%s" % jfz_id)

    async def parse(self, response: Response):
        try:
            data = response.html
            if data is None:
                self.logger.info("采集失败. url:%s" % response.url)
                return None
            if not data[2]['isLogin']:
                self.logger.warning("登录超时, 需要重新登录!")
                await self.login()
                return
            if data[0] != 10000:
                self.logger.info("采集失败. url:%s" % response.url)
                return None
            else:
                data = data[2]
            self.logger.debug('开始解析响应. url:%s' % response.url)
            if data['isLogin'] and data['isVerify']:
                data = data['hcData']
                _id = response.metadata['_id']
                jfz_id = response.metadata['jfz_id']
                tasks = []
                tasks_flag = []
                update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for item in data:
                    date = datetime.datetime.fromtimestamp(item['x'] / 1000).strftime('%Y%m%d')
                    row = {
                        'nav': float(item['unitNet']),
                        'sum_nav': float(item['accNet']),
                        'update_time': update_time
                    }
                    tasks.append(UpdateOne({'fund_id': _id, 'date': date}, {'$set': row}, upsert=True))
                    task = make_task_persist_update_detail(_id=jfz_id, source='jfz', update_time=update_time)
                    tasks_flag.append(task)
                async with self.sem:
                    s = time.time()
                    await self.id_map_collection.bulk_write(tasks_flag)
                    await self.nav_collection.bulk_write(tasks)
                    e = time.time()
                    self.logger.info("采集基金[%s]数据, 条数: [%s], 存储耗时:%s s" % (jfz_id, len(data), round(e-s, 2)))
                return
            else:
                self.logger.info("采集失败. url:%s" % response.url)
                return
        except Exception as e:
            self.logger.warning("采集失败. url:%s" % response.url)
            self.logger.exception(e)
            return


"""
累计净值接口:
https://www.jfz.com/simu/chart?id=P6281mbsw2
所有净值接口(需要登录):
https://www.jfz.com/simu/simuProductNew/GetPrdNetWorthDrawDown?prdCode=P6281mbsw2

"""


async def before_stop(spider):
    if spider.request_session:
        await spider.request_session.close()


if __name__ == '__main__':
    NavSpider.start(before_stop=before_stop)
