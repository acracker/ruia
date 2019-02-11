#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-01-30 15:49
# @Author  : pang
# @File    : items.py
# @Software: PyCharm

import re
import json
import logging
from ruia import AttrField, TextField, Item


class FundItem(Item):
    """
    定义目标字段抓取规则
    """
    rows = TextField(xpath_select='//tr')

    async def clean_rows(self, value):
        """
        清洗目标数据
        :param value: 初始目标数据
        :return:
        """
        result = []
        pattern = re.compile(r'.*?p-(.*?)\.html')
        try:
            for tr in value[1:]:
                columns = tr.getchildren()
                if len(columns) != 11:
                    continue
                item = {}
                for idx, td in enumerate(columns):
                    if idx == 2:
                        # 基金简称
                        content = dict(td.getchildren()[0].items())
                        item['short_name'] = content['title']
                        item['href'] = content['href']
                        match = re.match(pattern, item['href'])
                        if match:
                            item['id'] = match.group(1)
                    elif idx == 3:
                        # 投资策略
                        item['strategy'] = td.text
                    elif idx == 4:
                        # 投顾信息
                        content = td.getchildren()
                        if len(content) == 1:
                            content = dict(content[0].items())
                            item['company_short_name'] = content['title']
                            item['href_company'] = content['href']
                        else:
                            item['company_short_name'] = None
                            item['href_company'] = None
                    elif idx > 4:
                        result.append(item)
                        break
        except Exception as e:
            logging.exception(e)
        # {'short_name': '鸿凯激进9号', 'href': '/simu/p-P6281mbsw2.html', 'strategy': '管理期货',
        # 'company_short_name': '鸿凯投资', 'href_company': '/simu/c-CO00000179.html'}
        return result


class FundInfoItemV1(Item):
    """
    定义目标字段抓取规则
    """
    product_info = TextField(xpath_select='//div[@class="title"]/@data-prd-info')

    async def clean_product_info(self, value):
        """
        清洗目标数据
        :param value: 初始目标数据
        :return:
        """
        result = None
        try:
            result = json.loads(value)
        except Exception as e:
            logging.exception(e)
        # {'prd_name': '鸿凯激进9号', 'full_name': '鸿凯激进9号私募证券投资基金', 'prd_code': 'P6281mbsw2',
        # 'fund_dc_id': 'P6281mbsw2', 'build_date': '2017-10-31', 'index_code': 'CCFI', 'mng_dc_id': ['M5pqj0oyhw'],
        # 'com_code': 'CO00000179', 'com_dc_id': 'C5pqsxx018', 'register_number': 'SX3245', 'live_ids': ['385', '413']}
        return result


async def main():
    with open('demo.html', encoding='utf8') as f:
        string = "".join(f.readlines())
    items = await FundInfoItemV1.get_item(html=string)
    return items


if __name__ == '__main__':
    import asyncio
    asyncio.get_event_loop().run_until_complete(main())
