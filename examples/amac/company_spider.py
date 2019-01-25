#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-01-16 16:42
# @Author  : pang
# @File    : company_spider.py
# @Software: PyCharm
import asyncio
import logging
import re
import shelve
from collections import OrderedDict

from ruia import Spider, Response

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

lock = asyncio.Lock()
_result = shelve.open(r'D:\work\code\ruia\examples\amac\data\result.dat')


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

    async def start_requests(self):
        codes = ['P1003313',
                 'P1001430',
                 'P1003401',
                 'P1000549',
                 'P1010769',
                 'P1007915',
                 'P1007271',
                 'P1018488',
                 'P1000369',
                 'P1007822',
                 'P1005784',
                 'P1004070',
                 'P1002462',
                 'P1016372',
                 'P1016068',
                 'P1026018',
                 'P1016966',
                 'P1033450',
                 'P1004055',
                 'P1006164',
                 'P1062959',
                 'P1004037',
                 'P1033577',
                 'P1020090',
                 'P1032649',
                 'P1034187',
                 'P1033995',
                 'P1005206',
                 'P1063130',
                 'P1014385',
                 'P1060704',
                 'P1030053',
                 'P1008275',
                 'P1005008',
                 'P1005933',
                 'P1022101',
                 'P1004950',
                 'P1000361',
                 'P1065938',
                 'P1004526',
                 'P1002468',
                 'P1000652',
                 'P1002449',
                 'P1006040',
                 'P1003464',
                 'P1027224',
                 'P1064763',
                 'P1004150',
                 'P1031188',
                 'P1025836',
                 'P1023936',
                 'P1000891',
                 'P1064525',
                 'P1032021',
                 'P1034593',
                 'P1024169',
                 'P1005906',
                 'P1011157',
                 'P1008220',
                 'P1006148',
                 'P1001404',
                 'P1004789',
                 'P1026632',
                 'P1007210',
                 'P1005659',
                 'P1000306',
                 'P1006735',
                 'P1014760',
                 'P1029043',
                 'P1003486',
                 'P1010118',
                 'P1000290',
                 'P1032283',
                 'P1008265',
                 'P1010969',
                 'P1064874',
                 'P1061686',
                 'P1031924',
                 'P1006143',
                 'P1018021',
                 'P1016658',
                 'P1031309',
                 'P1016657',
                 'P1012599',
                 'P1034574',
                 'P1001739',
                 'P1028054',
                 'P1010078',
                 'P1033887',
                 'P1018728',
                 'P1000404',
                 'P1002344',
                 'P1016146',
                 'P1016131',
                 'P1003406',
                 'P1006674',
                 'P1000774',
                 'P1019324',
                 'P1004907',
                 'P1003342',
                 'P1008117',
                 'P1025719',
                 'P1062363',
                 'P1032361',
                 'P1066782',
                 'P1065664',
                 'P1062078',
                 'P1013825',
                 'P1024549',
                 'P1023137',
                 'P1015392',
                 'P1021817',
                 'P1006545',
                 'P1030978',
                 'P1064545',
                 'P1011224',
                 'P1068488',
                 'P1010760',
                 'P1066068',
                 'P1009064', ]
        for company_code in codes:
            company = await self.search_company(company_code)
            if len(company) == 1:
                company_id = company[0]['id']
                request = self.make_requests_from_url(url=url_company_detail.format(company_id=company[0]['id']),
                                                      headers=headers_company_detail, metadata={'company_code': company_code})
                yield request
            else:
                logging.warning('投顾查找失败. company_code:%s' % company_code)

    async def parse(self, response: Response):
        title = response.html_etree.xpath('//td[@class="td-title"]')
        content = response.html_etree.xpath('//td[@class="td-content"]')
        result = OrderedDict()
        company_code = response.metadata['company_code']
        for k, v in zip(title, content):
            result[k.text] = v
        company_name = result['基金管理人全称(中文):'].xpath('//div[@id="complaint1"]')[0].text
        # company_name = re.sub('')
        company_name = re.sub(r'&[a-z]{4}', '', company_name)
        company_name = re.sub(r'\s', '', company_name)
        qualification = result['是否为符合提供投资建议条件的第三方机构:'].text
        async with lock:
            _result[company_code] = (company_name, qualification)
        return None

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
    for k in _result:
        print("%s, %s, %s" % (k, _result[k][0], _result[k][1]))
    _result.close()
