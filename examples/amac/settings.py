#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-02-11 11:27
# @Author  : pang
# @File    : settings.py
# @Software: PyCharm

import os

# 数据来源, 表名前缀 以及字段前缀
SOURCE = "amac"

# mongo 地址
MONGODB_URL = os.environ.get('MONGODB_URL')
if not MONGODB_URL:
    MONGODB_URL = "mongodb://192.168.1.251:27017"
# mongo 数据库名称
DB_NAME = "privately_fund"
HTTP_PROXY = "http://16FDNCRS:234379@n5.t.16yun.cn:6441"


