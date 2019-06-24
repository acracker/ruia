#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-19 11:09
# @Author  : pang
import logging
import aiohttp

UPDATE_COUNSELOR_URL = "http://easy.gaoyusoft.com:10000/yitou/v1/counselor/save"
# UPDATE_COUNSELOR_URL = "http://192.168.1.130:9000/yitou/v1/counselor/save"


def under2camel(under_string):
    array = under_string.split('_')
    return ''.join(array[:1] + list(w.capitalize() or '_' for w in array[1:]))


print(under2camel(''))


async def update_counselor(**kwargs):
    body = {}
    columns = ['counselorCode',
               'counselorShortName',
               'counselorName',
               'registerNumber',
               'artificialPersonName',
               'isPrivate',
               'amacUrl',
               'counselorEstablishDate',
               'officeAddress',
               'officeCity',
               'officeProvince',
               'officeCoordinate',
               'registerDate',
               'registerAddress',
               'registerCity',
               'registerProvince',
               'registerCoordinate',
               'investStrategy',
               'fundCount',
               'fundScale',
               'createTime',
               'orgId',
               'introduction',
               'contactsName',
               'contactsPosition',
               'contactsPhone',
               'contactsEmail',
               'isConcern',
               'scoreCounter',
               'fundCounter',
               'grade',
               'tag',
               'extInfo',
               'organizationCode',
               'registeredCapital',
               'contributedCapital',
               'enterpriseProperty',
               'proportionOfRegisteredCapital',
               'fullTimeStaff',
               'fundQualificationStaff',
               'updateLatestDate',
               'counselorUrl',
               'counselorType',
               'isAmacMember',
               'isInvestmentAdvice',
               'isIntegrity',
               ]
    for k, v in kwargs.items():
        # col = under2camel(k)
        col = k
        if col not in columns:
            continue
        body[col] = v
    logging.info("保存投顾信息. data:%s" % str(body))
    async with aiohttp.ClientSession() as session:
        async with session.post(UPDATE_COUNSELOR_URL, json=body) as resp:
            text = await resp.text()
            print(text)