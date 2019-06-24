#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-18 10:57
# @Author  : pang


import datetime
import json
import os
import re
import random

import sys
from ruia import Spider, Response

from crawler.provider.internal import update_counselor


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


def fix_text(text):
    if text is None:
        return ""
    text = re.sub(r'<.*?>', "", text)
    text = re.sub(r"\s", "", text)
    return text


class CompanySpider(Spider):
    ALL = 1000
    SEARCH = 1001

    request_config = {
        'RETRIES': 1,
        'DELAY': 3,
        'TIMEOUT': 20
    }
    concurrency = 3
    name = 'company_spider'
    # kwargs = {
    #     'proxy': HTTP_PROXY,
    # }
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

    def __init__(self, middleware=None, loop=None, is_async_start=False, **kwargs):
        super().__init__(middleware, loop, is_async_start, **kwargs)
        self.result = {}
        self.action = None

    async def start_requests(self):
        action = self.settings.get('action', self.ALL)
        self.action = action
        if action == self.ALL:
            async for request in self.spawn_all_requests():
                yield request
        elif action == self.SEARCH:
            keyword = self.settings.get('action_params', {}).get('keyword', '平安道远投资管')
            yield await self.spawn_search_request(keyword)

    async def spawn_all_requests(self):
        num = await self.get_total_pages()
        for i in range(num):
            url = "http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand={rand}&page={page}&size=20".format(rand=random.random(), page=i)
            yield self.make_requests_from_url(url, data=b"{}", method="POST", res_type='json')

    async def get_total_pages(self):
        url = "http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand={rand}&page=0&size=20".format(rand=random.random())
        request = self.make_requests_from_url(url, data=b"{}", method="POST", res_type='json')
        resp = await request.fetch()
        if resp.status == 200:
            if resp.json and 'totalPages' in resp.json:
                return resp.json['totalPages']
        raise ValueError('failed to get total pages.')

    async def persist(self, data):
        if self.action == self.ALL:
            for item in data:
                company_name = item['company_name']
                row = {
                    'counselorName': company_name,
                    'isPrivate': 0,
                    # 'counselorShortName': item['company_name']
                    'registerNumber': item['register_number'],
                    'artificialPersonName': item['artificial_person_name'],
                    'amacUrl': item['url'],
                    'counselorEstablishDate': item['establish_date'],
                    'officeAddress': item['office_address'],
                    'officeCity': item['office_city'],
                    'officeProvince': item['office_province'],
                    'officeCoordinate': item['office_coordinate'],
                    'registerDate': item['register_date'],
                    'registerAddress': item['register_address'],
                    'registerCity': item['register_city'],
                    'registerProvince': item['register_province'],
                    'registerCoordinate': item['reg_coordinate'],
                    'fundCount': item['fund_count'],
                    'fundScale': item['fund_scale'],
                    'registeredCapital': item['registered_capital'],
                    'contributedCapital': item['contributed_capital'],
                    'enterpriseProperty': item['enterprise_property'],
                    'counselorType': item['counselor_type'],
                    'proportionOfRegisteredCapital': item['proportion_of_registered_capital'],
                    'fullTimeStaff': item['full_time_staff'],
                    'fundQualificationStaff': item['fund_qualification_staff'],
                    'counselorUrl': item['counselor_url'],
                    'organizationCode': item['organization_code'],
                    'isInvestmentAdvice': item['is_investment_advice'],
                    'updateLatestDate': item['update_latest_date'],
                    'isAmacMember': item['is_amac_member'],
                    'isIntegrity': item['is_integrity'],
                    'extInfo': json.dumps(item['ext_info']),
                }
                await update_counselor(**row)
        elif self.action == self.SEARCH:
            self.result = data

    async def parse(self, response: Response):
        data = response.json
        if data is None or 'content' not in data:
            self.logger.info("采集失败. url:%s" % response.url)
            return None
        try:
            data = data['content']
            result = []
            update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            for item in data:
                row = dict()
                row['company_name'] = fix_text(item['managerName'])
                row['artificial_person_name'] = item['artificialPersonName']
                row['register_number'] = fix_text(item['registerNo'])
                try:
                    row['establish_date'] = datetime.datetime.fromtimestamp(item['establishDate'] / 1000).strftime("%Y%m%d")
                except:
                    row['establish_date'] = item['establishDate']
                row['manager_has_product'] = item['managerHasProduct']
                # http://gs.amac.org.cn/amac-infodisc/res/pof/manager/101000000138.html
                item['id'] = item['url'].replace(".html", "")
                row['url'] = url_company_detail.format(company_id=item['id'])
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
                detail = await self.crawl_company_detail(item['id'])
                row['organization_code'] = detail.get('组织机构代码', '')
                row['registered_capital'] = detail.get('注册资本(万元)(人民币)', '')
                row['contributed_capital'] = detail.get('实缴资本(万元)(人民币)', '')
                row['enterprise_property'] = detail.get('企业性质', '')
                row['counselor_type'] = detail.get('机构类型', '')
                row['proportion_of_registered_capital'] = detail.get('注册资本实缴比例', '')
                row['full_time_staff'] = detail.get('全职员工人数', '')
                row['fund_qualification_staff'] = detail.get('取得基金从业人数', '')
                row['counselor_url'] = detail.get('机构网址', '')
                row['update_latest_date'] = detail.get('机构信息最后更新时间', '')
                row['is_amac_member'] = detail.get('是否为会员', '')
                row['is_investment_advice'] = detail.get('是否为符合提供投资建议条件的第三方机构', '')
                if len(detail.get('机构诚信信息', [])) >=2:
                    row['is_integrity'] = 0
                else:
                    row['is_integrity'] = 1
                try:
                    row['ext_info'] = {
                        '会员信息': {'是否为会员': detail['是否为会员'], '会员代表': detail.get('会员代表', ''), '当前会员类型': detail.get("当前会员类型", ""), '入会时间': detail.get("入会时间", "")},
                        '高管信息': {
                            '法定代表人/执行事务合伙人(委派代表)姓名': detail['法定代表人/执行事务合伙人(委派代表)姓名'],
                            '是否有基金从业资格': detail['是否有基金从业资格'],
                            '资格取得方式': detail['资格取得方式'],
                            '高管情况': detail['高管情况'],
                            '法定代表人/执行事务合伙人(委派代表)工作履历': detail['法定代表人/执行事务合伙人(委派代表)工作履历'],
                        },
                        "机构诚信信息": detail.get("机构诚信信息", [])
                    }
                except Exception as e:
                    self.logger.exception(e)
                    row['ext_info'] = {}
                result.append(row)
            await self.persist(result)
        except Exception as e:
            self.logger.info("采集失败. url:%s" % response.url)
            self.logger.exception(e)
            await self.stop()

    async def spawn_search_request(self, keyword=None):
        keyword = keyword or self.settings.get('action_params', {}).get('keyword', '平安道远投资管')
        body = {"keyword": keyword}
        request = self.make_requests_from_url(url=url_search_manager, method='POST',
                                              meta=body, headers=headers_search_company,
                                              json=body)
        return request

    async def parse_search(self, response: Response):
        data = response.json
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
            self.logger.warning("投顾搜索失败. keyword:%s" % response.meta['keyword'])
        await self.persist(result)

    async def crawl_company_detail(self, company_id="101000000138"):
        request = self.make_requests_from_url(url=url_company_detail.format(company_id=company_id), headers=headers_company_detail)
        response = await request.fetch()
        title = response.html_etree.xpath('//td[@class="td-title"]')
        content = response.html_etree.xpath('//td[@class="td-content"]')
        result = dict()
        for k, v in zip(title, content):
            key = str(k.text)
            key = re.sub(r'[:| ：]', '', key)
            key = re.sub(r'\s', '', key)
            text = v.text
            if text is None:
                text = ""
            else:
                text = re.sub(r'\s', '', text)
            if key == "高管情况":
                _th = v.xpath(".//th")
                _td = v.xpath(".//td")
                resp = []
                row = {}
                for idx, _v in enumerate(_td):
                    i = idx % len(_th)
                    if i == 0:
                        row = {}
                    _k = fix_text(_th[i].text)
                    _v = fix_text(_v.text)
                    row[_k] = _v
                    if i == len(_th) -1:
                        resp.append(row)
                result[key] = resp
            elif key == '法定代表人/执行事务合伙人(委派代表)工作履历':
                _th = v.xpath(".//th")
                _td = v.xpath(".//td")
                resp = []
                row = {}
                for idx, _v in enumerate(_td):
                    i = idx % len(_th)
                    if i == 0:
                        row = {}
                    _k = fix_text(_th[i].text)
                    _v = fix_text(_v.text)
                    row[_k] = _v
                    if i == len(_th) - 1:
                        resp.append(row)
                result[key] = resp
            elif key == "机构网址":
                v = v.xpath('.//a')
                if len(v) == 0:
                    result[key] = ""
                else:
                    result[key] = v[0].text
            elif key == "机构诚信信息":
                resp = []
                for _v in v.xpath(".//span"):
                    resp.append(fix_text(_v.text))
                result[key] = resp
            else:
                result[key] = text
        return result


if __name__ == '__main__':
    instance = CompanySpider.start(action=CompanySpider.ALL)
    print(len(instance.result))
