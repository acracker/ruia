#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-01-16 16:42
# @Author  : pang
# @File    : company_spider.py
# @Software: PyCharm

import re
from ruia import Request, Spider, Response


class CompanySpider(Spider):
    request_config = {
        'RETRIES': 0,
        'DELAY': 0,
        'TIMEOUT': 20
    }
    concurrency = 10

    kwargs = {}
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive',
               'Host': 'www.jfz.com', 'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'}

    async def get_total_pages(self):
        request = self.make_requests_from_url("https://www.jfz.com/simu/company_p1.html")
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
        # print("todo")   # todo
        # num = 1
        for i in range(1, num+1):
            url = "https://www.jfz.com/simu/company_p%s.html" % i
            yield self.make_requests_from_url(url=url)

    async def parse(self, response: Response):
        etree = response.html_etree
        elements = etree.xpath('//td[@class="t-company"]/a')
        for element in elements:
            print(element.items())


if __name__ == '__main__':
    CompanySpider.start()
