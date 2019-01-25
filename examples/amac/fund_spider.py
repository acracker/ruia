#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-01-17 13:49
# @Author  : pang
# @File    : fund.py
# @Software: PyCharm

import random
import re

from ruia import Spider, Response


# http://gs.amac.org.cn/amac-infodisc/api/pof/fund?rand=0.03935877331629101&page=0&size=20

class FundSpider(Spider):
    request_config = {
        'RETRIES': 0,
        'DELAY': 0,
        'TIMEOUT': 20
    }
    concurrency = 10
    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive', 'Content-Length': '2', 'Content-Type': 'application/json', 'Host': 'gs.amac.org.cn',
               'Origin': 'http://gs.amac.org.cn', 'Referer': 'http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'}

    async def get_total_pages(self):
        url = "http://gs.amac.org.cn/amac-infodisc/api/pof/fund?rand={rand}&page=0&size=20".format(rand=random.random())
        request = self.make_requests_from_url(url, method="POST")
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
        print("todo")  # todo
        num = 1
        for i in range(1, num + 1):
            url = "https://www.jfz.com/simu/company_p%s.html" % i
            yield self.make_requests_from_url(url=url)

    async def parse(self, response: Response):
        etree = response.html_etree
        elements = etree.xpath('//td[@class="t-company"]/a')
        for element in elements:
            print(element.items())


if __name__ == '__main__':
    FundSpider.start()
