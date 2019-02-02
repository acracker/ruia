#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-01-30 15:49
# @Author  : pang
# @File    : items.py
# @Software: PyCharm

import re
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


async def main():
    string = """
    <!DOCTYPE html>
    <!--[if IE 8]><html class="ie8" lang="en"><![endif]-->
    <!--[if IE 7]><html class="ie7" lang="en"><![endif]-->
    <!--[if !IE]><!--><html lang="en"><!--<![endif]-->
    <head>
    		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    		<meta name="renderer" content="webkit">
    		<meta http-equiv="X-UA-Compatible" content="IE=edge, chrome=1">
    		<meta name="viewport" content="user-scalable=yes,width=1200" />
    		<meta property="qc:admins" content="2037021714621665216375" /><!--QQConnect-->
            <meta name="baidu-site-verification" content="z4RVR7Qerf" />
            <meta name="sogou_site_verification" content="KS1HCJQJz9"/>
                    <meta name="360-site-verification" content="50c122d5c65da497ffa6172547e0ccc8" />
                    <meta name="glb_vip_uid" content="0"/>
            <meta name="jfz_rsv_token" content="a7f46d95bb698de0964a321e330a7535d838cb6b"/>
            <link rel="dns-prefetch" href="https://st.jfz.com" />
            <link rel="dns-prefetch" href="https://st.jinfuzi.com" />
            <script type="text/javascript">var jfz={}; jfz.version='2.4.1';</script>
            <script type="text/javascript">var GCertiToPassWord='1';</script>
    		<meta name="keywords" content="最近1年私募基金排行榜， 二级市场 私募基金业绩走势，私募产品收益排名" />
    <meta name="description" content="找最近1年二级市场 私募基金排行榜就上金斧子，支持各维度私募产品筛选，为您提供私募产品收益排名，私募基金最新净值及业绩走势，助您快速找到适合您的阳光私募基金。" />
    <link rel="Shortcut Icon" href="//st.jinfuzi.com/res/img/common/favicon.ico" />
    <link rel="stylesheet" type="text/css" href="//st.jinfuzi.com/res/css/common/common.css?v=2.4.1" />
    <link rel="stylesheet" type="text/css" href="//st.jinfuzi.com/res/css/oldcss/comm/modal.css?v=2.4.1" />
    <link rel="stylesheet" type="text/css" href="//st.jinfuzi.com/res/css/productCenter/productCenter.css?v=2.4.1" />
    <link rel="stylesheet" type="text/css" href="/assets/72cddf33/pager.css" />
    <script type="text/javascript" src="//st.jinfuzi.com/res/js/config.js?v=2.4.1"></script>
    <script type="text/javascript" src="//st.jinfuzi.com/res/js/lib/require.js?v=2.4.1"></script>
    <script type="text/javascript" src="//st.jinfuzi.com/res/js/service/common.js?v=2.4.1"></script>
    <script type="text/javascript" src="//st.jinfuzi.com/res/js/util/code_monitor.js?v=2.4.1"></script>
    <title>最近1年私募基金排行榜_私募产品收益排名_二级市场私募基金业绩走势-金斧子私募</title>
            	</head>
        	<body class="date_20190130 jfz anniversary-2019">

            <script>
                                        (function(){
                                            var bp = document.createElement('script');
                                            var curProtocol = window.location.protocol.split(':')[0];
                                            if (curProtocol === 'https') {
                                                bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';        
                                            }
                                            else {
                                                bp.src = 'http://push.zhanzhang.baidu.com/push.js';
                                            }
                                            var s = document.getElementsByTagName('script')[0];
                                            s.parentNode.insertBefore(bp, s);
                                        })();
                                        </script>
                                            <!-- Begin .g-topbar -->
    <div class="g-topbar">
        <div class="container clearfix">
            <div class="g-topbar-l">
                <div class="notice">欢迎您来到金斧子，投资有风险，选择需谨慎！</div>
            </div>
            <div class="g-topbar-r">
                <ul class="nav-list clearfix">
                    <li class="nav-item nav-item-reserve">
                        <a class="js-reserve" href="javascript:void(0);" data-biz="4" data-title="领取资产增值方案" data-ps="官网顶部通栏：领取资产增值方案" title="领取资产增值方案" rel="nofollow">领取资产增值方案</a>
                    </li>
                    <li class="nav-item nav-item-verify">
                        <a class="js-login" href="javascript:void(0);" data-title="登录">验证理财师真伪</a>
                        <a class="js-consultant-verify" href="javascript:void(0);" data-title="验证理财师真伪" style="display: none;">验证理财师真伪</a>
                    </li>
                    <li class="nav-item-logout nav-item"><a href="https://passport.jinfuzi.com/passport/user/login" rel="nofollow">登录</a></li>
                    <li class="nav-item-logout nav-item-pipe"></li>
                    <li class="nav-item-logout nav-item"><a href="https://passport.jinfuzi.com/passport/register/index" rel="nofollow">注册</a></li>
                    <li class="nav-item-logout nav-item-pipe"></li>
                    <li class="nav-item nav-item-dropdown nav-item-login" style="display: none;">
                        <span class="caption"><span class="username">金斧子</span><i class="caret"></i></span>
                        <div class="dropdown-layer">
                            <ul class="menu-list">
                                <li class="menu-item"><a target="_blank" href="/vipCenter/wealthCenter" rel="nofollow"><i class="menu-ico menu-ico-user"></i>账户中心</a></li>
                                <li class="menu-item"><a target="_blank" href="/questionnaire.html" rel="nofollow"><i class="menu-ico menu-ico-gear"></i>风险测评</a></li>
                                <li class="menu-item"><a target="_blank" id="js-topbar-forum" href="https://v.jfz.com" rel="nofollow"><i class="menu-ico menu-ico-comment"></i>我的社区</a></li>
                                <li class="menu-item">
                                                                        <a href="https://passport.jinfuzi.com/passport/user/logout?jto=https%3A%2F%2Fwww.jfz.com%2Fsimu%2Flist_w1_r1_p1.html" rel="nofollow">
                                                                        <i class="menu-ico menu-ico-power"></i>退出</a>
                                </li>
                            </ul>
                        </div>
                    </li>
                    <li class="nav-item"><a target="_blank" href="/public/about/index.html" rel="nofollow">关于我们</a></li>
                    <li class="nav-item-pipe"></li>
                    <li class="nav-item nav-item-dropdown nav-item-app">
                        <a href="javascript:void(0);" rel="nofollow">旗下APP</a>
                        <div class="dropdown-layer" style="width:115px" >
                            <div class="qrcode-wrap">
                                <div class="qrcode"><img src="//st.jinfuzi.com/res/img/common/qrcode/app_jfz_caifu_float.png" alt=""></div>
                                <div class="text">金斧子财富</div>
                            </div>
                                                    <!-- <div class="qrcode-wrap">
                                <div class="qrcode"><img src="//st.jinfuzi.com/res/img/common/qrcode/app_gxq_jfz.png" alt=""></div>
                                <div class="text">滚雪球基金</div>
                            </div> -->
                                                </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
    <!-- End .g-topbar -->


        <!-- Begin .g-header -->
        <div class="g-header g-header-full">
            <div class="container">
                <div class="main-wrap clearfix">
                    <div class="logo-wrap">
                                                <a class="logo-main" href="/"></a>
                                            <div class="logo-extend"></div>
                    </div>

                    <div class="search-wrap">
                        <form action="/search/index/simuindex.html" target="_blank" class="search-form">
                            <div class="search-key-wrap">
                                 <input id="longSearchInput"  maxlength="30" autocomplete="off" type="text" name="kw" placeholder="搜索净值/产品/基金经理/公司/视频" class="search-key" value="">
                            </div>
                            <div class="search-helper">
                                <ul class="search-helper-list"></ul>
                            </div>
                            <input class="search-btn" type="submit" value="确定">
                        </form>
                        <div class="search-hot">
                            <ul class="hot-list clearfix">
                                                                                                    <li class="hot-item"><a target="_blank" href="https://www.jfz.com/simu/tg-205.html">三大指数布局</a></li>
                                                                        <li class="hot-item"><a target="_blank" href="https://www.jfz.com/simu/tg-239.html">全明星FOF</a></li>
                                                                        <li class="hot-item"><a target="_blank" href="https://www.jfz.com/pevc/tg-62.html">独角兽精选</a></li>
                                                                        <li class="hot-item"><a target="_blank" href="https://www.jfz.com/simu/tg-237.html">展弘投资</a></li>
                                                                                        </ul>
                        </div>
                    </div>
                    <div class="hotline">
                        <i class="hotline-ico"></i>
                        <p class="number">400-9302-888</p>
                        <p class="text">咨询热线</p>
                    </div>
                </div>

                <div class="cats-wrap">
                    <div class="cats-list clearfix">
                        <dl class="cats-item cats-item--2">
                            <dt class="subject">在售产品</dt>
                            <dd class="content">
                                <a  class="" href="/sale/simu.html">阳光私募</a>
    <!--                            '/haiwai/index/index',array('id'=>5)-->
                                <a target="_blank" href="/simu/tg-brz640.html">海外移民</a>
                                <a class="" href="/sale/pevc.html">私募股权</a>
                                <a target="_blank" href="/hwym/detail-9.html">海外房产</a>
                            </dd>
                        </dl>
                        <dl class="cats-item cats-item--2">
                            <dt class="subject">私募证券</dt>
                            <dd class="content">
                                <a class="current" href="https://www.jfz.com/simu/list_w1_r1.html">私募排行</a>
                                <a class="" href="https://www.jfz.com/simu/company.html">私募公司</a>
                                <a class="" href="https://www.jfz.com/simu/manager.html">私募经理</a>
                                <a class="" href="/simu/billboard.html">私募榜单</a>
                            </dd>
                        </dl>
                        <dl class="cats-item cats-item--2">
                            <dt class="subject">私募股权</dt>
                            <dd class="content">
                                <a class="" href="/pe/gs.html">
                                    股权机构
                                </a>
                                <a class="" href="/pe/djs.html">
                                    独角兽公司<i class="menu-new"></i>
                                </a>
                                <a class="" href="/pe/cygs.html">
                                    创业公司
                                </a>
                                <a target="_blank" class="" href="/mujijin/">水星母基金</a>
                            </dd>
                        </dl>
                        <dl class="cats-item cats-item--no-subject">
                            <dd class="content">
                                <a target="_blank" class="link-secondary" href="https://v.jfz.com">私募社区<i class="menu-hot"></i></a>
                                <a class="link-secondary " href="/zhibo.html">私募视频</a>
                                <a class="link-secondary " href="/simu/xt.html?type=0">私募学堂</a>
                            </dd>
                        </dl>
                    </div>
                </div>
            </div>
        </div>
        <!-- End .g-header -->

            <div class="g-header g-header-small">
            <div class="container">
                <div class="main-wrap clearfix">
                    <div class="logo-wrap">
                                            <a class="logo-main" href="/"></a>
                                            <div class="logo-extend"></div>
                    </div>
                    <div class="menu-wrap">
                        <div class="menu-main">
                            <ul class="menu-list clearfix">
                               <li class="menu-list__item menu-list__item--has-dropdown">
                                   <a href="javascript:void(0);">在售产品</a>
                                   <div class="dwn-wrap">
                                       <ul class="dwn-list">
                                           <li class="dwn-list__item "><a href="/sale/simu.html">阳光私募</a></li>
                                           <li class="dwn-list__item "><a href="/sale/pevc.html">私募股权</a></li>
                                           <li target="_blank" class="dwn-list__item"><a target="_blank" href="/simu/tg-brz640.html">海外移民</a></li>
                                           <li target="_blank" class="dwn-list__item"><a target="_blank" href="/hwym/detail-7.html">海外房产</a></li>
                                       </ul>
                                   </div>
                               </li>
                               <li class="menu-list__item menu-list__item--has-dropdown">
                                   <a href="javascript:void(0);">私募证券</a>
                                   <div class="dwn-wrap">
                                       <ul class="dwn-list">
                                           <li class="dwn-list__item dwn-list__item--active"><a href="https://www.jfz.com/simu/list_w1_r1.html">私募排行</a></li>
                                           <li class="dwn-list__item "><a href="https://www.jfz.com/simu/company.html">私募公司</a></li>
                                           <li class="dwn-list__item "><a href="https://www.jfz.com/simu/manager.html">私募经理</a></li>
                                           <li class="dwn-list__item "><a href="/simu/billboard.html">私募榜单</a></li>
                                       </ul>
                                   </div>
                               </li>
                               <li class="menu-list__item menu-list__item--has-dropdown">
                                   <a href="javascript:void(0);">私募股权</a>
                                   <div class="dwn-wrap">
                                       <ul class="dwn-list">
                                           <li class="dwn-list__item "><a href="/pe/gs.html">股权机构</a></li>
                                           <li class="dwn-list__item "><a href="/pe/cygs.html">创业公司</a></li>
                                           <li class="dwn-list__item "><a href="/pe/djs.html">独角兽公司</a></li>
                                           <li class="dwn-list__item"><a target="_blank" href="/mujijin/">水星母基金</a></li>
                                       </ul>
                                   </div>
                               </li>
                            </ul>
                        </div>
                        <div class="menu-sub">
                            <ul class="menu-list clearfix">
                               <li class="menu-list__item"><a class="link-secondary" target="_blank" href="https://v.jfz.com">私募社区<i class="menu-new"></i></a></li>
                               <li class="menu-list__item"><a class="link-secondary" href="/zhibo.html">私募视频</a></li>
                               <li class="menu-list__item"><a class="link-secondary" href="/simu/xt.html?type=0">私募学堂</a></li>
                            </ul>
                        </div>
                    </div>

                    <div class="search-wrap">
                        <form action="/search/index/simuindex.html" target="_blank" class="search-form">
                            <div class="search-key-wrap">
                                <input type="text" maxlength="30" name="kw" autocomplete="off"  placeholder="请输入关键词" class="search-key" id="shortSearchInput">
                            </div>
                            <div class="search-helper">
                                <ul class="search-helper-list">
                                </ul>
                            </div>
                            <input class="search-btn" type="submit" value="确定">
                        </form>
                    </div>
                </div>
            </div>
        </div>
        <!-- Begin .w-toolbar -->
    <div class="w-toolbar">
        <ul>
            <li class="w-toolbar-item service" id="js-call-meiqia" rel="nofollow">
                <b id="unreadMsgCount">0</b>
                <style type="text/css">
                    #js-call-meiqia {
                        position: relative;
                    }

                    #unreadMsgCount {
                        display: none;
                        position: absolute;
                        top: -5px;
                        right: -10px;
                        width: 16px;
                        height: 16px;
                        font-size: 12px;
                        line-height: 14px;
                        text-align: center;
                        color: #fff;
                        border-radius: 50%;
                        background-color: #cd0202;
                    }
                </style>
                <script type='text/javascript'>
                    (function (m, ei, q, i, a, j, s) {
                        m[i] = m[i] || function () {
                            (m[i].a = m[i].a || []).push(arguments)
                        };
                        j = ei.createElement(q);
                        s = ei.getElementsByTagName(q)[0];
                        j.async = true;
                        j.charset = 'UTF-8';
                        j.src = 'https://static.meiqia.com/dist/meiqia.js?_=t';
                        s.parentNode.insertBefore(j, s);

                    })(window, document, 'script', '_MEIQIA');
                    _MEIQIA('assign', {groupToken: '25d94278b290a1210abfa8ef66aef228'});//设置默认的客服组
                    _MEIQIA('getUnreadMsg', function (msg) {
                        var text = '',
                            num = 0;
                        if (msg === 'hasBeenRead') { // 消息已被阅读
                            num = 0;
                        } else if (typeof(msg) === 'object') {
                            var unreadNum = document.getElementById('unreadNum').innerHTML,
                                lastMsg = msg[msg.length - 1];
                            num = isNaN(+unreadNum) ? msg.length : +unreadNum + msg.length;
                            // content_type 是消息的类型：
                            // text（文字）、photo（图片）、file（文件）
                            // content 是消息的内容
                            if (lastMsg.content_type === 'text') {
                                // 文字消息中可能会存在表情图片，由于路径问题
                                // 将文字消息中的图片处理为文字'[表情]'
                                text = lastMsg.content.replace(
                                    /<img [^>]*src=['"]([^'"]+)[^>]*>/gi, '[表情]'
                                );
                            } else if (lastMsg.content_type === 'photo') {
                                text = '[图片]';
                            } else if (lastMsg.content_type === 'file') {
                                text = '[文件]';
                            } else {
                                text = '[新消息]';
                            }
                        }
                        // 未读消息数量
                        document.getElementById('unreadMsgCount').innerHTML = num;
                        // 最后一条消息的内容
                        // document.getElementById('unreadMsg').innerHTML = text;
                    });
                    _MEIQIA('entId', 7283);
                    _MEIQIA('withoutBtn');
                    _MEIQIA('allSet', function () {
                        var __outerBtn = document.getElementById('js-call-meiqia');

                        __outerBtn.onclick = function () {
                            _MEIQIA('showPanel');
                        };
                    });
                </script>
            </li>
            <li class="w-toolbar-item app">
                <a class="caption" href="javascript:void(0);" rel="nofollow"><i class="app-ico"></i>手机APP</a>
                <span class="qrcode-wrap">
                        <span class="qrcode">
                           <i class="caret"><i class="caret"></i></i>
                           <img src="//st.jinfuzi.com/res/img/common/qrcode/app_jfz_caifu_float.png" alt="">
                        </span>
                    </span>
            </li>
            <li class="w-toolbar-item fav">
                <a href="/zixuan.html" rel="nofollow" target="_blank"><span class="caption"><i class="fav-ico"></i>自选产品</span></a>
            </li>
            <!-- <li class="w-toolbar-item gift">
                <a class="caption" href="javascript:void(0);" rel="nofollow"><i class="gift-ico"></i>新人福利</a>
                <form class="subscribe" id="newbieSubscribeFlotage" action="/public/rsv">
                    <div class="error-placement">
                        <div id="sub_name_error" style="display: none;">请输入手机号码</div>
                        <div id="sub_phone_error" style="display: none;"></div>
                    </div>
                    <div class="legend">免费定制资产配置方案</div>
                    <div class="input-group">
                        <div class="input-wrap">
                            <div class="input-control">
                                <input type="text" id="sub_name" class="input-text" placeholder="请输入2-5字中文姓名">
                            </div>
                        </div>
                        <div class="input-wrap">
                            <div class="input-control">
                                <input type="text" id="sub_phone" class="input-text" maxlength="11" placeholder="请输入11位手机号码">
                            </div>
                        </div>
                    </div>
                    <a href="javascript:void(0);" class="subscribe-submit" id="newbieSubscribeFlotageSubmit">提交</a>
                    <a href="javascript:void(0);" class="subscribe-close">&times;</a>
                </form>
            </li> -->
            <li class="w-toolbar-item hotline">
                <a class="caption" href="javascript:void(0);" rel="nofollow"><i class="tel-ico"></i>客服热线</a>
                <span class="text-wrap">
                    <span class="text">
                        <i class="caret"><i class="caret"></i></i>
                        <span>400-9302-888</span>
                    </span>
                </span>
            </li>
            <li class="w-toolbar-item backtop hover" onclick="window.scrollTo(0,0)"><a class="back-ico"></a></li>
        </ul>
    </div>
    <!-- End .w-toolbar -->
    <div class="p-products-center p--inset-shadow">
        <div class="container">
            <div class="p-products-data">
                <!-- Begin .filter -->
    <div class="tab filter filter-tab">
        <div class="tab-bd">
            <div class="tab-pane is-active">
                <div class="filter__item clearfix">
                    <div class="filter__item-subject">排行维度：</div>
                    <div class="filter__item-content">
                        <ul class="opts">
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_r1.html" rel="nofollow">不限</a></li>
                                                        <li class="opt is-selected"><a href="https://www.jfz.com/simu/list_w1_r1.html" rel="nofollow">二级市场</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w3_r1.html" rel="nofollow">海外</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w4_r1.html" rel="nofollow">新三板</a></li>
                                                </ul>
                    </div>
                </div>
                <div class="filter__item clearfix">
                    <div class="filter__item-subject">投资策略：</div>
                    <div class="filter__item-content">
                        <ul class="opts">
                                                    <li class="opt is-selected"><a href="https://www.jfz.com/simu/list_w1_r1.html" rel="nofollow">不限</a></li>
                                                    <li class="opt"><a href="https://www.jfz.com/simu/list_w1_d1_r1.html" rel="nofollow">股票策略</a></li>
                                                    <li class="opt"><a href="https://www.jfz.com/simu/list_w1_d2_r1.html" rel="nofollow">宏观策略</a></li>
                                                    <li class="opt"><a href="https://www.jfz.com/simu/list_w1_d3_r1.html" rel="nofollow">管理期货</a></li>
                                                    <li class="opt"><a href="https://www.jfz.com/simu/list_w1_d5_r1.html" rel="nofollow">相对价值策略</a></li>
                                                    <li class="opt"><a href="https://www.jfz.com/simu/list_w1_d6_r1.html" rel="nofollow">债券策略</a></li>
                                                    <li class="opt"><a href="https://www.jfz.com/simu/list_w1_d7_r1.html" rel="nofollow">组合策略</a></li>
                                                    <li class="opt"><a href="https://www.jfz.com/simu/list_w1_d8_r1.html" rel="nofollow">复合策略</a></li>
                                                </ul>
                    </div>
                </div>
                <div class="filter__item clearfix">
                    <div class="filter__item-subject">排名周期：</div>
                    <div class="filter__item-content">
                        <ul class="opts">
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w1.html" rel="nofollow">不限</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r2019.html" rel="nofollow">今年以来</a></li>
                                                        <li class="opt is-selected"><a href="https://www.jfz.com/simu/list_w1_r1.html" rel="nofollow">最近1年</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r2.html" rel="nofollow">最近2年</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r7.html" rel="nofollow">最近3年</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r9.html" rel="nofollow">成立以来</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r4.html" rel="nofollow">最近1月</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r5.html" rel="nofollow">最近3月</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r6.html" rel="nofollow">最近6月</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r2018.html" rel="nofollow">2018</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r2017.html" rel="nofollow">2017</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r2016.html" rel="nofollow">2016</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r2015.html" rel="nofollow">2015</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r2014.html" rel="nofollow">2014</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r2013.html" rel="nofollow">2013</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r2012.html" rel="nofollow">2012</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r2011.html" rel="nofollow">2011</a></li>
                                                </ul>
                    </div>
                </div>
                <div class="filter__item clearfix">
                    <div class="filter__item-subject">年化收益：</div>
                    <div class="filter__item-content">
                        <ul class="opts">
                                                        <li class="opt is-selected"><a href="https://www.jfz.com/simu/list_w1_r1.html" rel="nofollow">不限</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r1_y1.html" rel="nofollow">50%以上</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r1_y2.html" rel="nofollow">40%-50%</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r1_y3.html" rel="nofollow">30%-40%</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r1_y4.html" rel="nofollow">20%-30%</a></li>
                                                        <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r1_y5.html" rel="nofollow">10%-20%</a></li>
                                                </ul>
                    </div>
                </div>
                <div class="filter__item clearfix">
                    <div class="filter__item-subject">更多设置：</div>
                    <div class="filter__item-content"><a class="tri js-filter-more" href="javascript:void(0);"></a></div>
                </div>

                <div class="filter__item--extra hide">
                    <div class="filter__item clearfix">
                        <div class="filter__item-subject">成立时间：</div>
                        <div class="filter__item-content">
                            <ul class="opts">
                                                                <li class="opt is-selected"><a href="https://www.jfz.com/simu/list_w1_r1.html" rel="nofollow">不限</a></li>
                                                                <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r1_t1.html" rel="nofollow">1年以内</a></li>
                                                                <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r1_t2.html" rel="nofollow">1~3年</a></li>
                                                                <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r1_t3.html" rel="nofollow">3~5年</a></li>
                                                                <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r1_t4.html" rel="nofollow">5年以上</a></li>
                                                        </ul>
                        </div>
                    </div>
                    <div class="filter__item clearfix">
                        <div class="filter__item-subject">所在地区：</div>
                        <div class="filter__item-content">
                            <ul class="opts">
                                                                <li class="opt is-selected"><a href="https://www.jfz.com/simu/list_w1_r1.html" rel="nofollow">不限</a></li>
                                                                <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r1_c1.html" rel="nofollow">北京</a></li>
                                                                <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r1_c2.html" rel="nofollow">上海</a></li>
                                                                <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r1_c3.html" rel="nofollow">深圳</a></li>
                                                                <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r1_c4.html" rel="nofollow">广州</a></li>
                                                        </ul>
                        </div>
                    </div>
                    <div class="filter__item clearfix">
                        <div class="filter__item-subject">是否分级：</div>
                        <div class="filter__item-content">
                            <ul class="opts">
                                                                <li class="opt is-selected"><a href="https://www.jfz.com/simu/list_w1_r1.html" rel="nofollow">不限</a></li>
                                                                <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r1_i1.html" rel="nofollow">分级</a></li>
                                                                <li class="opt"><a href="https://www.jfz.com/simu/list_w1_r1_i2.html" rel="nofollow">不分级</a></li>
                                                        </ul>
                        </div>
                    </div>
                </div>

                <div class="filter__item clearfix">
                    <div class="filter__item-subject">已选条件：</div>
                    <div class="filter__item-content">
                        <ul class="opts">
                                                                                        <li class="opt is-active"><a href="https://www.jfz.com/simu/list_r1.html">二级市场<i>&times;</i></a></li>
                                                                <li class="opt is-active"><a href="https://www.jfz.com/simu/list_w1.html">最近1年<i>&times;</i></a></li>
                                                            <li class="opt reset"><a href="https://www.jfz.com/simu/list.html">清空条件</a></li>

                            <li class="opt">共<span class="text-highlight">12710</span>款产品满足条件</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- End .filter -->

    <!-- Begin .filter-feature -->
        <div class="filter-feature ">
            <div class="filter__item clearfix">
                <div class="filter__item-subject">特色筛选：</div>
                <div class="filter__item-content">
                    <ul class="opts">
                                                <li class="opt">
                                <label for="award_250">
                                    <input class="js-feature"
                                           type="checkbox"
                                           id="award_250"
                                           name="award_label[]"
                                           value="250"
                                           data-url="https://www.jfz.com/simu/list_w1_r1.html?flag=tag"
                                        >
                                    <a>单周涨幅超5%</a>
                                </label>
                            </li>
                                                <li class="opt">
                                <label for="award_20">
                                    <input class="js-feature"
                                           type="checkbox"
                                           id="award_20"
                                           name="award_label[]"
                                           value="20"
                                           data-url="https://www.jfz.com/simu/list_w1_r1.html?flag=tag"
                                        >
                                    <a>4433好基金</a>
                                </label>
                            </li>
                                                <li class="opt">
                                <label for="award_16">
                                    <input class="js-feature"
                                           type="checkbox"
                                           id="award_16"
                                           name="award_label[]"
                                           value="16"
                                           data-url="https://www.jfz.com/simu/list_w1_r1.html?flag=tag"
                                        >
                                    <a>年化>20%</a>
                                </label>
                            </li>
                                                <li class="opt">
                                <label for="award_15">
                                    <input class="js-feature"
                                           type="checkbox"
                                           id="award_15"
                                           name="award_label[]"
                                           value="15"
                                           data-url="https://www.jfz.com/simu/list_w1_r1.html?flag=tag"
                                        >
                                    <a>净值创新高</a>
                                </label>
                            </li>
                                                <li class="opt">
                                <label for="award_8">
                                    <input class="js-feature"
                                           type="checkbox"
                                           id="award_8"
                                           name="award_label[]"
                                           value="8"
                                           data-url="https://www.jfz.com/simu/list_w1_r1.html?flag=tag"
                                        >
                                    <a>价值投资</a>
                                </label>
                            </li>
                                                <li class="opt">
                                <label for="award_6">
                                    <input class="js-feature"
                                           type="checkbox"
                                           id="award_6"
                                           name="award_label[]"
                                           value="6"
                                           data-url="https://www.jfz.com/simu/list_w1_r1.html?flag=tag"
                                        >
                                    <a>稳健型私募</a>
                                </label>
                            </li>
                                                <li class="opt">
                                <label for="award_10">
                                    <input class="js-feature"
                                           type="checkbox"
                                           id="award_10"
                                           name="award_label[]"
                                           value="10"
                                           data-url="https://www.jfz.com/simu/list_w1_r1.html?flag=tag"
                                        >
                                    <a>金长江奖</a>
                                </label>
                            </li>
                                                <li class="opt">
                                <label for="award_4">
                                    <input class="js-feature"
                                           type="checkbox"
                                           id="award_4"
                                           name="award_label[]"
                                           value="4"
                                           data-url="https://www.jfz.com/simu/list_w1_r1.html?flag=tag"
                                        >
                                    <a>金阳光奖</a>
                                </label>
                            </li>
                                                <li class="opt">
                                <label for="award_12">
                                    <input class="js-feature"
                                           type="checkbox"
                                           id="award_12"
                                           name="award_label[]"
                                           value="12"
                                           data-url="https://www.jfz.com/simu/list_w1_r1.html?flag=tag"
                                        >
                                    <a>金牛机构代表作</a>
                                </label>
                            </li>
                                                <li class="opt">
                                <label for="award_13">
                                    <input class="js-feature"
                                           type="checkbox"
                                           id="award_13"
                                           name="award_label[]"
                                           value="13"
                                           data-url="https://www.jfz.com/simu/list_w1_r1.html?flag=tag"
                                        >
                                    <a>热销产品</a>
                                </label>
                            </li>
                                                <li class="opt">
                                <label for="award_17">
                                    <input class="js-feature"
                                           type="checkbox"
                                           id="award_17"
                                           name="award_label[]"
                                           value="17"
                                           data-url="https://www.jfz.com/simu/list_w1_r1.html?flag=tag"
                                        >
                                    <a>百亿机构</a>
                                </label>
                            </li>
                                                <li class="opt">
                                <label for="award_18">
                                    <input class="js-feature"
                                           type="checkbox"
                                           id="award_18"
                                           name="award_label[]"
                                           value="18"
                                           data-url="https://www.jfz.com/simu/list_w1_r1.html?flag=tag"
                                        >
                                    <a>海外产品</a>
                                </label>
                            </li>
                                                <li class="opt">
                                <label for="award_19">
                                    <input class="js-feature"
                                           type="checkbox"
                                           id="award_19"
                                           name="award_label[]"
                                           value="19"
                                           data-url="https://www.jfz.com/simu/list_w1_r1.html?flag=tag"
                                        >
                                    <a>热搜产品</a>
                                </label>
                            </li>
                                                <li class="opt">
                                <label for="award_21">
                                    <input class="js-feature"
                                           type="checkbox"
                                           id="award_21"
                                           name="award_label[]"
                                           value="21"
                                           data-url="https://www.jfz.com/simu/list_w1_r1.html?flag=tag"
                                        >
                                    <a>公奔私</a>
                                </label>
                            </li>
                                                <li class="opt">
                                <label for="award_22">
                                    <input class="js-feature"
                                           type="checkbox"
                                           id="award_22"
                                           name="award_label[]"
                                           value="22"
                                           data-url="https://www.jfz.com/simu/list_w1_r1.html?flag=tag"
                                        >
                                    <a>老牌私募</a>
                                </label>
                            </li>
                                                <li class="opt">
                                <label for="award_23">
                                    <input class="js-feature"
                                           type="checkbox"
                                           id="award_23"
                                           name="award_label[]"
                                           value="23"
                                           data-url="https://www.jfz.com/simu/list_w1_r1.html?flag=tag"
                                        >
                                    <a>有止损线</a>
                                </label>
                            </li>
                                                <li class="opt">
                                <label for="award_24">
                                    <input class="js-feature"
                                           type="checkbox"
                                           id="award_24"
                                           name="award_label[]"
                                           value="24"
                                           data-url="https://www.jfz.com/simu/list_w1_r1.html?flag=tag"
                                        >
                                    <a>无认购费</a>
                                </label>
                            </li>
                                                <li class="opt">
                                <label for="award_25">
                                    <input class="js-feature"
                                           type="checkbox"
                                           id="award_25"
                                           name="award_label[]"
                                           value="25"
                                           data-url="https://www.jfz.com/simu/list_w1_r1.html?flag=tag"
                                        >
                                    <a>无封闭期</a>
                                </label>
                            </li>
                                            <li class="opt-more js-opt-more is-hide ">
                            <a href="javascript:void(0);">
                                展开更多                        </a>
                            <i class="ico ico-arr-2 ico-arr-2-down"></i>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    <!-- End .filter-feature -->

    <!-- Begin .filter-table -->
    <div class="filter-table">
        <table width="100%" summary="私募产品" class="table table-smcp-2">
            <thead>
                <tr>
                    <th class="t-compare">对比</th>
                    <th class="t-sn">序号</th>
                    <th class="t-name">基金简称</th>
                    <th class="t-strategy">投资策略</th>
                    <th class="t-company">投资顾问</th>
                    <th class="t-manager">基金经理</th>
                    <th class="t-runtime">运行时间</th>
                    <th class="t-net">最新净值</th>
                    <th class="t-total">
                        累计收益                </th>
                    <th class="t-year">
                        <a class="js-sort is-active" rel="nofollow" href="https://www.jfz.com/simu/list_w1_r1_s2.html">最近1年收益<i class="ico ico-sort"></i></a>                </th>
                    <th class="t-trend">净值走势</th>
                </tr>
            </thead>
            <tbody>
                                                <tr class="odd">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="P6281mbsw2" product_name="鸿凯激进9号" accumulate_profit="" />
                        </td>
                        <td class="t-sn">1</td>
                        <td class="t-name">
                            <a title="鸿凯激进9号" target="_blank" href="/simu/p-P6281mbsw2.html">鸿凯激进9号</a>                    </td>
                        <td class="t-strategy">管理期货</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-CO00000179.html"
                                       target="_blank" title="鸿凯投资">鸿凯投资</a>
                                                                            </td>
                        <td class="t-manager">
                                                        <a href="/simu/m-PL000002VM.html" target="_blank">林军</a>
                                                </td>
                        <td class="t-runtime">1年3月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="P6281mbsw2" data-target="trend_chart_P6281mbsw2">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_P6281mbsw2"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="even">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="22221AJ6" product_name="潮金产融1号" accumulate_profit="" />
                        </td>
                        <td class="t-sn">2</td>
                        <td class="t-name">
                            <a title="潮金产融1号" target="_blank" href="/simu/p-22221AJ6.html">潮金产融1号</a>                    </td>
                        <td class="t-strategy">股票策略</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-CO000001N0.html"
                                       target="_blank" title="潮金投资">潮金投资</a>
                                                                            </td>
                        <td class="t-manager">
                                                        <a href="/simu/m-M61u660zra.html" target="_blank">黄伟斌</a>
                                                </td>
                        <td class="t-runtime">2年6月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="22221AJ6" data-target="trend_chart_22221AJ6">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_22221AJ6"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="odd">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="222299ET" product_name="大禾投资掘金1号" accumulate_profit="" />
                        </td>
                        <td class="t-sn">3</td>
                        <td class="t-name">
                            <a title="大禾投资掘金1号" target="_blank" href="/simu/p-222299ET.html">大禾投资掘金1号</a>                    </td>
                        <td class="t-strategy">股票策略</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-CO00000HXZ.html"
                                       target="_blank" title="大禾投资">大禾投资</a>
                                                                            </td>
                        <td class="t-manager">
                                                        <a href="/simu/m-M617sraz9h.html" target="_blank">胡鲁滨</a>
                                                </td>
                        <td class="t-runtime">2年5月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="222299ET" data-target="trend_chart_222299ET">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_222299ET"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="even">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="222297DK" product_name="大禾投资掘金5号" accumulate_profit="" />
                        </td>
                        <td class="t-sn">4</td>
                        <td class="t-name">
                            <a title="大禾投资掘金5号" target="_blank" href="/simu/p-222297DK.html">大禾投资掘金5号</a>                    </td>
                        <td class="t-strategy">股票策略</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-CO00000HXZ.html"
                                       target="_blank" title="大禾投资">大禾投资</a>
                                                                            </td>
                        <td class="t-manager">
                                                        <a href="/simu/m-M617sraz9h.html" target="_blank">胡鲁滨</a>
                                                </td>
                        <td class="t-runtime">2年3月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="222297DK" data-target="trend_chart_222297DK">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_222297DK"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="odd">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="P6du8bg2os" product_name="涨乐零号" accumulate_profit="" />
                        </td>
                        <td class="t-sn">5</td>
                        <td class="t-name">
                            <a title="涨乐零号" target="_blank" href="/simu/p-P6du8bg2os.html">涨乐零号</a>                    </td>
                        <td class="t-strategy">复合策略</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-CO00000AY5.html"
                                       target="_blank" title="泽铭投资">泽铭投资</a>
                                                                            </td>
                        <td class="t-manager">
                                                        ---
                                                </td>
                        <td class="t-runtime">1年</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="P6du8bg2os" data-target="trend_chart_P6du8bg2os">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_P6du8bg2os"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="even">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="22221USR" product_name="云南信托-赛纳债投资" accumulate_profit="" />
                        </td>
                        <td class="t-sn">6</td>
                        <td class="t-name">
                            <a title="云南信托-赛纳债投资" target="_blank" href="/simu/p-22221USR.html">云南信托-赛纳债投资</a>                    </td>
                        <td class="t-strategy">债券策略</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-CO000000D9.html"
                                       target="_blank" title="云南信托">云南信托</a>
                                                                            </td>
                        <td class="t-manager">
                                                        ---
                                                </td>
                        <td class="t-runtime">3年1月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="22221USR" data-target="trend_chart_22221USR">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_22221USR"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="odd">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="P623oi9tzw" product_name="大禾投资掘金6号" accumulate_profit="" />
                        </td>
                        <td class="t-sn">7</td>
                        <td class="t-name">
                            <a title="大禾投资掘金6号" target="_blank" href="/simu/p-P623oi9tzw.html">大禾投资掘金6号</a>                    </td>
                        <td class="t-strategy">股票策略</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-CO00000HXZ.html"
                                       target="_blank" title="大禾投资">大禾投资</a>
                                                                            </td>
                        <td class="t-manager">
                                                        <a href="/simu/m-M617sraz9h.html" target="_blank">胡鲁滨</a>
                                                </td>
                        <td class="t-runtime">1年4月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="P623oi9tzw" data-target="trend_chart_P623oi9tzw">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_P623oi9tzw"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="even">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="P6dybia9eb" product_name="辰翔锐进1号" accumulate_profit="" />
                        </td>
                        <td class="t-sn">8</td>
                        <td class="t-name">
                            <a title="辰翔锐进1号" target="_blank" href="/simu/p-P6dybia9eb.html">辰翔锐进1号</a>                    </td>
                        <td class="t-strategy">股票策略</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-CO00000JH6.html"
                                       target="_blank" title="辰翔投资">辰翔投资</a>
                                                                            </td>
                        <td class="t-manager">
                                                        ---
                                                </td>
                        <td class="t-runtime">1年</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="P6dybia9eb" data-target="trend_chart_P6dybia9eb">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_P6dybia9eb"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="odd">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="P6dybia4q4" product_name="中金量化-金然稳健1号" accumulate_profit="" />
                        </td>
                        <td class="t-sn">9</td>
                        <td class="t-name">
                            <a title="中金量化-金然稳健1号" target="_blank" href="/simu/p-P6dybia4q4.html">中金量化-金然稳健1号</a>                    </td>
                        <td class="t-strategy">管理期货</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-CO000003HU.html"
                                       target="_blank" title="中金量化">中金量化</a>
                                                                            </td>
                        <td class="t-manager">
                                                        ---
                                                </td>
                        <td class="t-runtime">1年1月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="P6dybia4q4" data-target="trend_chart_P6dybia4q4">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_P6dybia4q4"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="even">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="22222JDF" product_name="华银德洋基金" accumulate_profit="" />
                        </td>
                        <td class="t-sn">10</td>
                        <td class="t-name">
                            <a title="华银德洋基金" target="_blank" href="/simu/p-22222JDF.html">华银德洋基金</a>                    </td>
                        <td class="t-strategy">复合策略</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-CO000000G0.html"
                                       target="_blank" title="华银精治">华银精治</a>
                                                                            </td>
                        <td class="t-manager">
                                                        <a href="/simu/m-PL0000002D.html" target="_blank">丁洋</a>
                                                </td>
                        <td class="t-runtime">3年9月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="22222JDF" data-target="trend_chart_22222JDF">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_22222JDF"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="odd">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="P623v4f82h" product_name="大禾投资掘金7号" accumulate_profit="" />
                        </td>
                        <td class="t-sn">11</td>
                        <td class="t-name">
                            <a title="大禾投资掘金7号" target="_blank" href="/simu/p-P623v4f82h.html">大禾投资掘金7号</a>                    </td>
                        <td class="t-strategy">股票策略</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-CO00000HXZ.html"
                                       target="_blank" title="大禾投资">大禾投资</a>
                                                                            </td>
                        <td class="t-manager">
                                                        <a href="/simu/m-M617sraz9h.html" target="_blank">胡鲁滨</a>
                                                </td>
                        <td class="t-runtime">1年4月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="P623v4f82h" data-target="trend_chart_P623v4f82h">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_P623v4f82h"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="even">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="P6du8bg2ot" product_name="塑造者1号" accumulate_profit="" />
                        </td>
                        <td class="t-sn">12</td>
                        <td class="t-name">
                            <a title="塑造者1号" target="_blank" href="/simu/p-P6du8bg2ot.html">塑造者1号</a>                    </td>
                        <td class="t-strategy">相对价值策略</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-C62cbfb2th.html"
                                       target="_blank" title="合绎投资">合绎投资</a>
                                                                            </td>
                        <td class="t-manager">
                                                        ---
                                                </td>
                        <td class="t-runtime">1年1月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="P6du8bg2ot" data-target="trend_chart_P6du8bg2ot">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_P6du8bg2ot"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="odd">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="P6dybia5n1" product_name="宁水精选三期" accumulate_profit="" />
                        </td>
                        <td class="t-sn">13</td>
                        <td class="t-name">
                            <a title="宁水精选三期" target="_blank" href="/simu/p-P6dybia5n1.html">宁水精选三期</a>                    </td>
                        <td class="t-strategy">复合策略</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-CO00000F65.html"
                                       target="_blank" title="道富投资">道富投资</a>
                                                                            </td>
                        <td class="t-manager">
                                                        ---
                                                </td>
                        <td class="t-runtime">1年2月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="P6dybia5n1" data-target="trend_chart_P6dybia5n1">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_P6dybia5n1"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="even">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="22222O15" product_name="云梦泽-碧浪" accumulate_profit="" />
                        </td>
                        <td class="t-sn">14</td>
                        <td class="t-name">
                            <a title="云梦泽-碧浪" target="_blank" href="/simu/p-22222O15.html">云梦泽-碧浪</a>                    </td>
                        <td class="t-strategy">管理期货</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-CO00000AP8.html"
                                       target="_blank" title="信普资产">信普资产</a>
                                                                            </td>
                        <td class="t-manager">
                                                        <a href="/simu/m-PL00000217.html" target="_blank">毛君岳</a>
                                                </td>
                        <td class="t-runtime">3年7月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="22222O15" data-target="trend_chart_22222O15">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_22222O15"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="odd">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="P6dytp6qan" product_name="济凡玄武一号" accumulate_profit="" />
                        </td>
                        <td class="t-sn">15</td>
                        <td class="t-name">
                            <a title="济凡玄武一号" target="_blank" href="/simu/p-P6dytp6qan.html">济凡玄武一号</a>                    </td>
                        <td class="t-strategy">复合策略</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-C6240319g3.html"
                                       target="_blank" title="济凡资产">济凡资产</a>
                                                                            </td>
                        <td class="t-manager">
                                                        ---
                                                </td>
                        <td class="t-runtime">12月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="P6dytp6qan" data-target="trend_chart_P6dytp6qan">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_P6dytp6qan"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="even">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="P6dybia5ql" product_name="领冠三号" accumulate_profit="" />
                        </td>
                        <td class="t-sn">16</td>
                        <td class="t-name">
                            <a title="领冠三号" target="_blank" href="/simu/p-P6dybia5ql.html">领冠三号</a>                    </td>
                        <td class="t-strategy">股票策略</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-C623jjnskn.html"
                                       target="_blank" title="领冠投资">领冠投资</a>
                                                                            </td>
                        <td class="t-manager">
                                                        ---
                                                </td>
                        <td class="t-runtime">1年1月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="P6dybia5ql" data-target="trend_chart_P6dybia5ql">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_P6dybia5ql"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="odd">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="P61h64xs34" product_name="中珏安粮2号" accumulate_profit="" />
                        </td>
                        <td class="t-sn">17</td>
                        <td class="t-name">
                            <a title="中珏安粮2号" target="_blank" href="/simu/p-P61h64xs34.html">中珏安粮2号</a>                    </td>
                        <td class="t-strategy">管理期货</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-CO00000J9M.html"
                                       target="_blank" title="中珏投资">中珏投资</a>
                                                                            </td>
                        <td class="t-manager">
                                                        <a href="/simu/m-M61bsn2683.html" target="_blank">秦坤</a>
                                                </td>
                        <td class="t-runtime">1年9月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="P61h64xs34" data-target="trend_chart_P61h64xs34">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_P61h64xs34"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="even">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="P61zqa1zjn" product_name="量道富祥cta1号" accumulate_profit="" />
                        </td>
                        <td class="t-sn">18</td>
                        <td class="t-name">
                            <a title="量道富祥cta1号" target="_blank" href="/simu/p-P61zqa1zjn.html">量道富祥cta1号</a>                    </td>
                        <td class="t-strategy">管理期货</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-CO00000CSV.html"
                                       target="_blank" title="深圳量道投资">深圳量道投资</a>
                                                                            </td>
                        <td class="t-manager">
                                                        <a href="/simu/m-M6286kxudt.html" target="_blank">陈耀州</a>
                                                </td>
                        <td class="t-runtime">1年5月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="P61zqa1zjn" data-target="trend_chart_P61zqa1zjn">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_P61zqa1zjn"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="odd">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="P61c7iwaon" product_name="太平山1号" accumulate_profit="" />
                        </td>
                        <td class="t-sn">19</td>
                        <td class="t-name">
                            <a title="太平山1号" target="_blank" href="/simu/p-P61c7iwaon.html">太平山1号</a>                    </td>
                        <td class="t-strategy">组合策略</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-C617ueubr7.html"
                                       target="_blank" title="深圳云天志">深圳云天志</a>
                                                                            </td>
                        <td class="t-manager">
                                                        ---
                                                </td>
                        <td class="t-runtime">1年11月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="P61c7iwaon" data-target="trend_chart_P61c7iwaon">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_P61c7iwaon"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="even">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="P61gw7pp26" product_name="华融信托-现金宝1号" accumulate_profit="" />
                        </td>
                        <td class="t-sn">20</td>
                        <td class="t-name">
                            <a title="华融信托-现金宝1号" target="_blank" href="/simu/p-P61gw7pp26.html">华融信托-现金宝1号</a>                    </td>
                        <td class="t-strategy">股票策略</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-CO000000ER.html"
                                       target="_blank" title="华融信托">华融信托</a>
                                                                            </td>
                        <td class="t-manager">
                                                        ---
                                                </td>
                        <td class="t-runtime">1年10月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="P61gw7pp26" data-target="trend_chart_P61gw7pp26">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_P61gw7pp26"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="odd">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="P62dgrqrau" product_name="领冠二号" accumulate_profit="" />
                        </td>
                        <td class="t-sn">21</td>
                        <td class="t-name">
                            <a title="领冠二号" target="_blank" href="/simu/p-P62dgrqrau.html">领冠二号</a>                    </td>
                        <td class="t-strategy">股票策略</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-C623jjnskn.html"
                                       target="_blank" title="领冠投资">领冠投资</a>
                                                                            </td>
                        <td class="t-manager">
                                                        ---
                                                </td>
                        <td class="t-runtime">1年2月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="P62dgrqrau" data-target="trend_chart_P62dgrqrau">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_P62dgrqrau"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="even">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="P6240319fo" product_name="招金11号" accumulate_profit="" />
                        </td>
                        <td class="t-sn">22</td>
                        <td class="t-name">
                            <a title="招金11号" target="_blank" href="/simu/p-P6240319fo.html">招金11号</a>                    </td>
                        <td class="t-strategy">复合策略</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-CO0000099P.html"
                                       target="_blank" title="中仁资产">中仁资产</a>
                                                                            </td>
                        <td class="t-manager">
                                                        <a href="/simu/m-PL00000BNO.html" target="_blank">袁晓明</a>
                                                </td>
                        <td class="t-runtime">1年4月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="P6240319fo" data-target="trend_chart_P6240319fo">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_P6240319fo"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="odd">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="P612vssugi" product_name="泉汐名扬1号" accumulate_profit="" />
                        </td>
                        <td class="t-sn">23</td>
                        <td class="t-name">
                            <a title="泉汐名扬1号" target="_blank" href="/simu/p-P612vssugi.html">泉汐名扬1号</a>                    </td>
                        <td class="t-strategy">股票策略</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-C612vssufb.html"
                                       target="_blank" title="泉汐投资">泉汐投资</a>
                                                                            </td>
                        <td class="t-manager">
                                                        <a href="/simu/m-M628tqgpah.html" target="_blank">张扬</a>
                                                </td>
                        <td class="t-runtime">2年</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="P612vssugi" data-target="trend_chart_P612vssugi">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_P612vssugi"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="even">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="P6du8bg0yp" product_name="久盈3号" accumulate_profit="" />
                        </td>
                        <td class="t-sn">24</td>
                        <td class="t-name">
                            <a title="久盈3号" target="_blank" href="/simu/p-P6du8bg0yp.html">久盈3号</a>                    </td>
                        <td class="t-strategy">股票策略</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-C61bualipx.html"
                                       target="_blank" title="久盈(天津)">久盈(天津)</a>
                                                                            </td>
                        <td class="t-manager">
                                                        ---
                                                </td>
                        <td class="t-runtime">1年2月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="P6du8bg0yp" data-target="trend_chart_P6du8bg0yp">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_P6du8bg0yp"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                <tr class="odd">
                        <td class="t-compare">
                            <input class="tb_chk" name="compare[]" type="checkbox" id="222294XE" product_name="诺德FOHF5号" accumulate_profit="" />
                        </td>
                        <td class="t-sn">25</td>
                        <td class="t-name">
                            <a title="诺德FOHF5号" target="_blank" href="/simu/p-222294XE.html">诺德FOHF5号</a>                    </td>
                        <td class="t-strategy">组合策略</td>
                        <td class="t-company">
                                                                                        <a href="/simu/c-CO00000A7B.html"
                                       target="_blank" title="鸿鹏资本">鸿鹏资本</a>
                                                                            </td>
                        <td class="t-manager">
                                                        ---
                                                </td>
                        <td class="t-runtime">2年3月</td>
                        <td class="t-net">
                                                        <a class="require-risk-modal" href="javascript:void(0);">认证可见</a>
                                                </td>
                        <td class="t-total">
                            <span class="">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a>                        </span>
                        </td>
                        <td class="t-year">
                            <span class="text-highlight">
                                <a class="require-risk-modal" href="javascript:;">认证可见</a></span>
                        </td>

                        <td class="t-trend">
                            <div class="trend-viewer" data-id="222294XE" data-target="trend_chart_222294XE">
                                <div class="trend-viewer-hd"><i class="ico ico-trend"></i></div>
                                <div class="trend-viewer-bd">
                                    <i class="caret"><i class="caret"></i></i>
                                    <div class="chart-wrap" id="trend_chart_222294XE"></div>
                                </div>
                            </div>
                        </td>
                    </tr>
                                    </tbody>
        </table>
    </div>
    <!-- End .filter-table -->

        <div class="pagination-wrapper">
            <div class="pagination-inner">
                <ul class="page-list" id="yw0"><li class="page-item page-first disabled"><a href="https://www.jfz.com/simu/list_w1_r1.html"></a></li>
    <li class="page-item page-prev disabled"><a href="https://www.jfz.com/simu/list_w1_r1.html"></a></li>
    <li class="page-item active"><a href="https://www.jfz.com/simu/list_w1_r1.html">1</a></li>
    <li class="page-item"><a href="https://www.jfz.com/simu/list_w1_r1_p2.html">2</a></li>
    <li class="page-item"><a href="https://www.jfz.com/simu/list_w1_r1_p3.html">3</a></li>
    <li class="page-item"><a href="https://www.jfz.com/simu/list_w1_r1_p4.html">4</a></li>
    <li class="page-item"><a href="https://www.jfz.com/simu/list_w1_r1_p5.html">5</a></li>
    <li class="page-item"><a href="https://www.jfz.com/simu/list_w1_r1_p6.html">6</a></li>
    <li class="page-item"><a href="https://www.jfz.com/simu/list_w1_r1_p7.html">7</a></li>
    <li class="page-item"><a href="https://www.jfz.com/simu/list_w1_r1_p8.html">8</a></li>
    <li class="page-item"><a href="https://www.jfz.com/simu/list_w1_r1_p9.html">9</a></li>
    <li class="page-item"><a href="https://www.jfz.com/simu/list_w1_r1_p10.html">10</a></li>
    <li class="page-item page-next"><a href="https://www.jfz.com/simu/list_w1_r1_p2.html"></a></li>
    <li class="page-item page-last"><a href="https://www.jfz.com/simu/list_w1_r1_p509.html"></a></li></ul>        </div>
        </div>
            </div>

            <!-- Begin .floor-topic -->
            <div class="floor floor-topic">
        <div class="floor-head clearfix">
            <div class="floor-head-bow">
                <div class="title"><i class="stick"></i><span class="caption">私募投资攻略</span></div>
            </div>
            <div class="floor-head-after"></div>
        </div>
        <div class="floor-cont">
            <div id="floor-topic-rmzt" class="mosaic-list clearfix">
                                <div data-dimension="430x325" class="mosaic-item mosaic-item-lg">
                        <div class="animate-scale figure"><a target="_blank" href="https://www.jfz.com/pevc/tg-62.html" rel="nofollow"><img src="https://jfz-static2.oss-cn-hangzhou.aliyuncs.com/main/img/3dc4a4a31688ac922869c4b72f792496.jpg" alt=""></a></div>
                        <div class="mosaic-item-title">
                            <a target="_blank" href="/zhuanti/item-2.html" class="u-hover u-label u-label-xs" rel="nofollow">股权</a>
                            <a target="_blank" href="https://www.jfz.com/pevc/tg-62.html" class="caption" title="【拥抱独角兽】即报即审，井喷上市！" rel="nofollow">【拥抱独角兽】即报即审，井喷上市！</a>
                        </div>
                    </div>
                                            <div data-dimension="230x140" class="mosaic-item">
                        <div class="animate-scale figure"><a target="_blank" href="https://www.jfz.com/simu/tg-202.html" rel="nofollow"><img src="https://jfz-static2.oss-cn-hangzhou.aliyuncs.com/main/img/39d5e9cadbd1eb4f2b2e1f953eae1b86.jpg" alt=""></a></div>
                        <div class="mosaic-item-title">
                            <a target="_blank" href="/zhuanti/item-1.html" class="u-hover u-label u-label-xs" rel="nofollow">私募</a>
                            <a target="_blank" href="https://www.jfz.com/simu/tg-202.html" class="caption" title="老牌机构：景林全球" rel="nofollow">老牌机构：景林全球</a>
                        </div>
                    </div>
                                <div data-dimension="230x140" class="mosaic-item">
                        <div class="animate-scale figure"><a target="_blank" href="https://www.jfz.com/simu/tg-277.html" rel="nofollow"><img src="https://jfz-static2.oss-cn-hangzhou.aliyuncs.com/main/img/7dbfb026b78ad6c3a702c50b51da95ea.jpg" alt=""></a></div>
                        <div class="mosaic-item-title">
                            <a target="_blank" href="/zhuanti/item-1.html" class="u-hover u-label u-label-xs" rel="nofollow">私募</a>
                            <a target="_blank" href="https://www.jfz.com/simu/tg-277.html" class="caption" title="布局A股好产品" rel="nofollow">布局A股好产品</a>
                        </div>
                    </div>
                                <div data-dimension="230x140" class="mosaic-item">
                        <div class="animate-scale figure"><a target="_blank" href="https://www.jfz.com/pevc/tg-63.html" rel="nofollow"><img src="https://jfz-static2.oss-cn-hangzhou.aliyuncs.com/main/img/debe92683abd279b44a9e44f4cd2500e.jpg" alt=""></a></div>
                        <div class="mosaic-item-title">
                            <a target="_blank" href="/zhuanti/item-2.html" class="u-hover u-label u-label-xs" rel="nofollow">股权</a>
                            <a target="_blank" href="https://www.jfz.com/pevc/tg-63.html" class="caption" title="精选股权明星项目" rel="nofollow">精选股权明星项目</a>
                        </div>
                    </div>
                                <div data-dimension="230x140" class="mosaic-item">
                        <div class="animate-scale figure"><a target="_blank" href="https://www.jfz.com/simu/tg-237.html" rel="nofollow"><img src="https://oss-cn-hangzhou.aliyuncs.com/jfzapp-static2/ad/ce3173c688d89b4ec3f5c26d2541a7c7.jpg" alt=""></a></div>
                        <div class="mosaic-item-title">
                            <a target="_blank" href="/zhuanti/item-1.html" class="u-hover u-label u-label-xs" rel="nofollow">私募</a>
                            <a target="_blank" href="https://www.jfz.com/simu/tg-237.html" class="caption" title="2018年每月都盈利" rel="nofollow">2018年每月都盈利</a>
                        </div>
                    </div>
                                <div data-dimension="230x140" class="mosaic-item">
                        <div class="animate-scale figure"><a target="_blank" href="https://www.jfz.com/simu/tg-276.html" rel="nofollow"><img src="https://jfz-static2.oss-cn-hangzhou.aliyuncs.com/main/img/d40a901d8dc76d8fbbfb98047087e322.jpg" alt=""></a></div>
                        <div class="mosaic-item-title">
                            <a target="_blank" href="/zhuanti/item-1.html" class="u-hover u-label u-label-xs" rel="nofollow">私募</a>
                            <a target="_blank" href="https://www.jfz.com/simu/tg-276.html" class="caption" title="财富传承利器" rel="nofollow">财富传承利器</a>
                        </div>
                    </div>
                                <div data-dimension="230x140" class="mosaic-item">
                        <div class="animate-scale figure"><a target="_blank" href="https://www.jfz.com/simu/tg-241.html" rel="nofollow"><img src="https://oss-cn-hangzhou.aliyuncs.com/jfzapp-static2/ad/2d10a6959afbb44775898354ebf64dc3.jpg" alt=""></a></div>
                        <div class="mosaic-item-title">
                            <a target="_blank" href="/zhuanti/item-1.html" class="u-hover u-label u-label-xs" rel="nofollow">私募</a>
                            <a target="_blank" href="https://www.jfz.com/simu/tg-241.html" class="caption" title="零管理费，连续正收益" rel="nofollow">零管理费，连续正收益</a>
                        </div>
                    </div>
                        </div>
        </div>
    </div>
    <!-- End .floor -->
            <!-- End .floor-topic -->

            <!--Begin seo-私募内链 -->
                <!-- Begin .g-navigation -->
        <div class="g-navigation">
            <div class="container">
                <div class="nav-wrap">
                    <table class="table">
                        <tbody>
                        <tr class="odd">
                            <th class="subject">当前私募频道介绍</th>
                            <td class="content">金斧子私募频道为您提供私募基金产品列表筛选，私募基金产品基本介绍及私募基金产品业绩等信息，助您快速找到最适合您的阳光私募基金。</td>
                        </tr>
                        <tr class="even">
                            <th class="subject">热门阳光私募产品</th>
                            <td class="content">
                                                            <ul class="items clearfix">
                                                                        <li class="item"><a title="展弘稳进1号9期" target="_blank" href="/simu/p-P6e3brupza.html">展弘稳进1号9期</a></li>
                                                                        <li class="item"><a title="九坤日享中证500指数增强1号" target="_blank" href="/simu/p-P61qejyj9e.html">九坤日享中证500指数增强1号</a></li>
                                                                        <li class="item"><a title="景林金色中国基金" target="_blank" href="/simu/p-222221LU.html">景林金色中国基金</a></li>
                                                                        <li class="item"><a title="源乐晟全球精选A期" target="_blank" href="/simu/p-1431401752.html">源乐晟全球精选A期</a></li>
                                                                        <li class="item"><a title="方圆增强收益基金" target="_blank" href="/simu/p-P61qhv18ag.html">方圆增强收益基金</a></li>
                                                                        <li class="item"><a title="九坤量化CTA1号" target="_blank" href="/simu/p-P61q9lchtt.html">九坤量化CTA1号</a></li>
                                                                        <li class="item"><a title="千象1期" target="_blank" href="/simu/p-P61m33fwxx.html">千象1期</a></li>
                                                                        <li class="item"><a title="信合全球" target="_blank" href="/simu/p-222229T1.html">信合全球</a></li>
                                                                        <li class="item"><a title="丰岭稳健成长8期" target="_blank" href="/simu/p-22221X3Y.html">丰岭稳健成长8期</a></li>
                                                                        <li class="item"><a title="逸杉2期" target="_blank" href="/simu/p-222213S8.html">逸杉2期</a></li>
                                                                        <li class="item"><a title="保银金斧子紫荆怒放1期" target="_blank" href="/simu/p-P62d56zbug.html">保银金斧子紫荆怒放1期</a></li>
                                                                        <li class="item"><a title="泊通成长7号" target="_blank" href="/simu/p-P61cwbyi3b.html">泊通成长7号</a></li>
                                                                        <li class="item"><a title="合晟同晖固定收益3号" target="_blank" href="/simu/p-22221G8C.html">合晟同晖固定收益3号</a></li>
                                                                        <li class="item"><a title="少数派29号" target="_blank" href="/simu/p-22221GPM.html">少数派29号</a></li>
                                                                        <li class="item"><a title="从容全天候联接A" target="_blank" href="/simu/p-P623v4f848.html">从容全天候联接A</a></li>
                                                                        <li class="item"><a title="九坤日享沪深300指数增强1号" target="_blank" href="/simu/p-P61q2z73sy.html">九坤日享沪深300指数增强1号</a></li>
                                                                        <li class="item"><a title="保银金斧子中国价值1期" target="_blank" href="/simu/p-P62d56zbue.html">保银金斧子中国价值1期</a></li>
                                                                        <li class="item"><a title="希瓦金山量化2号" target="_blank" href="/simu/p-P6241qko81.html">希瓦金山量化2号</a></li>
                                                                </ul>
                                                        </td>
                        </tr>
                        <tr class="odd">
                            <th class="subject">知名私募基金经理</th>
                            <td class="content">
                                                            <ul class="items clearfix">
                                                                        <li class="item"><a target="_blank" title="蒋锦志" href="/simu/m-PL0000000Z.html">蒋锦志</a></li>
                                                                        <li class="item"><a target="_blank" title="林军" href="/simu/m-PL000002VM.html">林军</a></li>
                                                                        <li class="item"><a target="_blank" title="曾晓洁" href="/simu/m-PL00000BNE.html">曾晓洁</a></li>
                                                                        <li class="item"><a target="_blank" title="王鹏辉" href="/simu/m-M5pqj0oyl3.html">王鹏辉</a></li>
                                                                        <li class="item"><a target="_blank" title="林成栋" href="/simu/m-M5pqj0oz1y.html">林成栋</a></li>
                                                                        <li class="item"><a target="_blank" title="辛宇" href="/simu/m-M5pqj0oxfw.html">辛宇</a></li>
                                                                        <li class="item"><a target="_blank" title="黄如洪" href="/simu/m-M5pqj0ozk3.html">黄如洪</a></li>
                                                                        <li class="item"><a target="_blank" title="吴星" href="/simu/m-M5pqj0oz1b.html">吴星</a></li>
                                                                        <li class="item"><a target="_blank" title="赵军" href="/simu/m-M5pqj0oymw.html">赵军</a></li>
                                                                        <li class="item"><a target="_blank" title="王林" href="/simu/m-PL00000BVT.html">王林</a></li>
                                                                        <li class="item"><a target="_blank" title="赵丹阳" href="/simu/m-M5pqj0ox4a.html">赵丹阳</a></li>
                                                                        <li class="item"><a target="_blank" title="王亚伟" href="/simu/m-M5pqj0ozjj.html">王亚伟</a></li>
                                                                        <li class="item"><a target="_blank" title="李泽刚" href="/simu/m-M5pqj0oybe.html">李泽刚</a></li>
                                                                        <li class="item"><a target="_blank" title="蔡明" href="/simu/m-M5pqj0oz04.html">蔡明</a></li>
                                                                        <li class="item"><a target="_blank" title="姚齐聪" href="/simu/m-PL000003OH.html">姚齐聪</a></li>
                                                                        <li class="item"><a target="_blank" title="金斌" href="/simu/m-PL000002X2.html">金斌</a></li>
                                                                        <li class="item"><a target="_blank" title="裘国根" href="/simu/m-PL00000095.html">裘国根</a></li>
                                                                        <li class="item"><a target="_blank" title="朱合伟" href="/simu/m-M612bycoht.html">朱合伟</a></li>
                                                                        <li class="item"><a target="_blank" title="张杰平" href="/simu/m-PL00000AM5.html">张杰平</a></li>
                                                                        <li class="item"><a target="_blank" title="但斌" href="/simu/m-M5pqj0oy1n.html">但斌</a></li>
                                                                </ul>
                                                        </td>
                        </tr>
                        <tr class="even">
                            <th class="subject">知名私募基金公司</th>
                            <td class="content">
                                                            <ul class="items clearfix">
                                                                        <li class="item"><a target="_blank" title="上海景林资产" href="/simu/c-CO000000FU.html">上海景林资产</a></li>
                                                                        <li class="item"><a target="_blank" title="展弘投资" href="/simu/c-CO000009RM.html">展弘投资</a></li>
                                                                        <li class="item"><a target="_blank" title="丰岭资本" href="/simu/c-CO00000182.html">丰岭资本</a></li>
                                                                        <li class="item"><a target="_blank" title="北京源乐晟资产" href="/simu/c-C5pqsxwzxj.html">北京源乐晟资产</a></li>
                                                                        <li class="item"><a target="_blank" title="合晟资产" href="/simu/c-CO000000X5.html">合晟资产</a></li>
                                                                        <li class="item"><a target="_blank" title="九坤投资" href="/simu/c-C5pqsxx0ea.html">九坤投资</a></li>
                                                                        <li class="item"><a target="_blank" title="和聚投资" href="/simu/c-C5pqsxwzrj.html">和聚投资</a></li>
                                                                        <li class="item"><a target="_blank" title="重阳投资" href="/simu/c-CO0000009D.html">重阳投资</a></li>
                                                                        <li class="item"><a target="_blank" title="淡水泉" href="/simu/c-CO0000000G.html">淡水泉</a></li>
                                                                        <li class="item"><a target="_blank" title="少薮派投资" href="/simu/c-CO000001HE.html">少薮派投资</a></li>
                                                                        <li class="item"><a target="_blank" title="上海保银投资" href="/simu/c-CO000000MU.html">上海保银投资</a></li>
                                                                        <li class="item"><a target="_blank" title="鸿凯投资" href="/simu/c-CO00000179.html">鸿凯投资</a></li>
                                                                        <li class="item"><a target="_blank" title="展博投资" href="/simu/c-C5pqsxx084.html">展博投资</a></li>
                                                                        <li class="item"><a target="_blank" title="星石投资" href="/simu/c-CO00000021.html">星石投资</a></li>
                                                                        <li class="item"><a target="_blank" title="牧鑫资产" href="/simu/c-CO00000EHR.html">牧鑫资产</a></li>
                                                                        <li class="item"><a target="_blank" title="千为投资" href="/simu/c-CO00000DA9.html">千为投资</a></li>
                                                                </ul>
                                                        </td>
                        </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <!-- End .g-navigation -->        <!-- End .seo-私募内链 -->
        </div>
    </div><!-- Begin .g-license -->
    <div class="g-license">
        <div class="container">
            <div class="header">
                <div class="title"><span class="caption">持牌机构&ensp;/&ensp;强大股东<span class="line-through"></span></span></div>
            </div>
            <div class="license-list-wrap">
                <ul class="license-list clearfix">
                    <li class="license-item license-item-sales">
                        <a rel="nofollow" target="_blank" href="/public/about/security.html" class="media">
                            <div class="media-object"></div>
                            <div class="media-body">
                                <div class="title">证监会批准</div>
                                <div class="subtitle">独立基金销售机构</div>
                            </div>
                        </a>
                    </li>
                    <li class="license-item license-item-csrc">
                        <a rel="nofollow" target="_blank" href="/public/about/security.html" class="media">
                            <div class="media-object"></div>
                            <div class="media-body">
                                <div class="title">监督机构</div>
                                <div class="subtitle">中国证券监督管理委员会</div>
                            </div>
                        </a>
                    </li>
                    <li class="license-item license-item-bank">
                        <a rel="nofollow" target="_blank" href="/public/about/security.html" class="media">
                            <div class="media-object"></div>
                            <div class="media-body">
                                <div class="title">安全监管银行</div>
                                <div class="subtitle">中国民生银行</div>
                            </div>
                        </a>
                    </li>
                    <li class="license-item license-item-self">
                        <a rel="nofollow" target="_blank" href="/public/about/security.html" class="media">
                            <div class="media-object"></div>
                            <div class="media-body">
                                <div class="title">自律组织</div>
                                <div class="subtitle">中国证券投资基金业协会</div>
                            </div>
                        </a>
                    </li>
                    <li class="license-item license-item-sequoia">
                        <a rel="nofollow" target="_blank" href="/public/about/stockholder.html" class="media">
                            <div class="media-object"></div>
                            <div class="media-body">
                                <div class="title">红杉资本</div>
                                <div class="subtitle">国际著名风投</div>
                            </div>
                        </a>
                    </li>
                    <li class="license-item license-item-cmb">
                        <a rel="nofollow" target="_blank" href="/public/about/stockholder.html" class="media">
                            <div class="media-object"></div>
                            <div class="media-body">
                                <div class="title">招商局创投</div>
                                <div class="subtitle">大型央企背景</div>
                            </div>
                        </a>
                    </li>
                    <li class="license-item license-item-hx">
                        <a rel="nofollow" target="_blank" href="/public/about/stockholder.html" class="media">
                            <div class="media-object"></div>
                            <div class="media-body">
                                <div class="title">华西股份</div>
                                <div class="subtitle">A股上市公司</div>
                            </div>
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
    <!-- End .g-license -->

    <!-- Begin .g-footer -->
    <div class="g-footer">
        <!-- Begin .container -->
        <div class="container clearfix">
            <!-- Begin .g-footer-main -->
            <div class="g-footer-logo">
                <div class="outer">
                    <div class="inner">
                                            <div class="figure"><img src="//st.jinfuzi.com/res/img/common/ft_logo.png" alt="金斧子 聪明你的投资"></div>
                                        </div>
                </div>
            </div>
            <!-- End .g-footer-logo -->
            <!-- Begin .g-footer-main -->
            <div class="g-footer-main">
                <!-- Begin .nav -->
                <div class="nav">
                    <ul class="nav-links clearfix">
                        <li class="item"><a rel="nofollow" target="_blank" href="/public/about/index.html">关于我们</a></li>
                        <li class="item-pipe"></li>
                        <li class="item"><a rel="nofollow" target="_blank" href="/public/about/stockholder.html">股东背景</a></li>
                        <li class="item-pipe"></li>
                        <li class="item"><a rel="nofollow" target="_blank" href="/public/about/news.html">媒体报道</a></li>
                        <li class="item-pipe"></li>
                        <li class="item"><a rel="nofollow" target="_blank" href="/public/about/jobsOpportunity.html">职业发展</a></li>
                        <li class="item-pipe"></li>
    <!--                    <li class="item"><a rel="nofollow" target="_blank" href="--><!--">联系我们</a></li>-->
    <!--                    <li class="item-pipe"></li>-->
                        <li class="item">
                                                        <a rel="nofollow" href="http://d.jfz.com"  target="_blank">私募申报</a>
                                                </li>
                    </ul>
                </div>
                <!-- End .nav -->
                <!-- Begin .services -->
                <div class="services clearfix">
                    <div class="subject">客服电话</div>
                    <div class="content">400-9302-888</div>
                </div>
                <!-- End .services -->
                <!-- Begin .social -->
                <div class="social clearfix">
                    <div class="subject">关注我们</div>
                    <div class="content">
                        <a rel="nofollow" class="social-item social-item-weixin" href="javascript:void(0);" style="z-index: 10">
                            <i class="social-icon social-icon-weixin"></i>
                                                    <div class="social-popup">
                                <i class="social-popup-caret"></i>
                                <div class="social-popup-cont clearfix">
                                    <div class="qrcode-wrap">
                                        <div class="qrcode"><img src="//st.jinfuzi.com/res/img/common/qrcode/app_jfz_wxapp.png" alt=""></div>
                                        <div class="text">小程序</div>
                                    </div>
                                    <div class="qrcode-wrap">
                                        <div class="qrcode"><img src="//st.jinfuzi.com/res/img/common/qrcode/wx_jfz_zx_f.jpg" alt=""></div>
                                        <div class="text">官方微信</div>
                                    </div>
                                </div>
                            </div>
                                                </a>
                                            <a rel="nofollow" target="_blank" class="social-item social-item-weibo" title="新浪微博" href="http://weibo.com/JFZofficial?topnav=1&wvr=6&topsug=1">
                            <i class="social-icon social-icon-weibo"></i>
                        </a>
                        <!--                    <a rel="nofollow" target="_blank" class="social-item social-item-tencent" title="腾讯微博" href="http://t.qq.com/jinfuzi000">-->
    <!--                        <i class="social-icon social-icon-tencent"></i>-->
    <!--                    </a>-->
                    </div>
                </div>
                <!-- End .social -->
                <!-- Begin .friend-links -->
                                            <div class="friend-links clearfix">
                        <div class="subject">友情链接:</div>
                        <div class="content">
                            <ul class="list">
                                                                <li class="item"><a target="_blank" href="https://www.jfz.com/pe/07P6f4b3h3i9.html?sign=yqlj">融通臻选基金</a></li>
                                                                <li class="item"><a target="_blank" href="https://www.jinfuzi.com/simu/tg-275?sign=gw-yqlj">富人退休养老规划</a></li>
                                                                <li class="item"><a target="_blank" href="https://www.jinfuzi.com/simu/tg-275?sign=gw-yqlj">泰康养老社区</a></li>
                                                                <li class="item"><a target="_blank" href="https://www.jfz.com/simu/list_d1_w1.html">阳光私募基金</a></li>
                                                                <li class="item"><a target="_blank" href="http://www.waitouwang.com/">海外房产</a></li>
                                                                <li class="item"><a target="_blank" href="https://www.jfz.com/cfgl.html">第三方理财</a></li>
                                                                <li class="item"><a target="_blank" href="https://m.jfz.com/bbs/">私募BBS</a></li>
                                                                <li class="item"><a target="_blank" href="https://v.jfz.com/">私募社区</a></li>
                                                                <li class="item"><a target="_blank" href="https://www.jfz.com/simu/list_r2018.html">2018私募基金排行榜</a></li>
                                                                <li class="item"><a target="_blank" href="https://www.jfz.com/simu/company.html">全国私募公司排名</a></li>
                                                                <li class="item"><a target="_blank" href="https://www.jfz.com/simu/list_r2017.html">2017私募基金排行榜</a></li>
                                                                <li class="item"><a target="_blank" href="http://www.jfz.com/simu/company_c4.html">深圳私募公司排名</a></li>
                                                                <li class="item"><a target="_blank" href="http://www.jfz.com/simu/company_c3.html">广州私募公司排名</a></li>
                                                                <li class="item"><a target="_blank" href="http://www.jfz.com/simu/company_c2.html">上海私募公司排名</a></li>
                                                                <li class="item"><a target="_blank" href="http://www.jfz.com/simu/company_c1.html">北京私募公司排名</a></li>
                                                                <li class="item"><a target="_blank" href="https://www.jfz.com/simu/manager.html">私募基金经理排名</a></li>
                                                                <li class="item"><a target="_blank" href="https://www.jfz.com/cfgl/detail-42.html">金斧子怎么样</a></li>
                                                                <li class="item"><a target="_blank" href="https://www.jfz.com/baike/">私募知识</a></li>
                                                                <li class="item"><a target="_blank" href="https://www.jfz.com/simu/billboard.html">私募基金排名</a></li>
                                                                <li class="item"><a target="_blank" href="https://www.jfz.com/cfgl/detail-2.html">好买财富</a></li>
                                                                <li class="item"><a target="_blank" href="https://www.jfz.com/cfgl/detail-4385.html">宜信财富</a></li>
                                                                <li class="item"><a target="_blank" href="https://www.jfz.com/pe/cygs.html">创业公司大全</a></li>
                                                                <li class="item"><a target="_blank" href="https://www.jfz.com/pe/djs.html">中国独角兽公司</a></li>
                                                                <li class="item"><a target="_blank" href="https://www.jfz.com/pe/gs.html">私募股权公司</a></li>
                                                        </ul>
                        </div>
                    </div>
                            <!-- End .friend-links -->
                <!-- Begin .copyrights -->
                <div class="copyrights">
                                        <p>&copy;2010-2017 www.jfz.com 深圳市<a target="_blank" href="https://www.jfz.com/index/">金斧子</a>基金销售有限公司版权所有</a>
                            <a rel="nofollow" target="_blank" href="http://www.miibeian.gov.cn/"> 粤ICP备 15076207号-4</a>
                            <a rel="nofollow" target="_blank" href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=44030502000148">
                                <img src="//st.jinfuzi.com/res/img/common/beian.png" style="vertical-align: top;">
                                <span>粤公网安备 44030502000148号</span>
                            </a>&nbsp;
                            <a rel="nofollow" target="_blank" href="https://szcert.ebs.org.cn/782ae405-2029-4f1a-b135-d963b1f9be4f">
                                <img src="//st.jinfuzi.com/res/img/common/wj.gif" width="20" height="27" border="0" style="vertical-align: top;">
                                <span>工商网监</span>
                            </a>
                        </p>
                                    <p>投资者应仔细阅读理财产品的法律文件，了解产品风险和收益特征（包括系统性风险和特定产品所特有的投资风险等）。投资者应根据自身资产状况、风险承受能力选择适合自己的理财产品。金斧子提供的宣传推介材料仅供投资者参考，不构成金斧子的任何推荐或投资建议。所有资料均来源于公开信息整理，市场有风险，投资需谨慎。</p>
                </div>
                <!-- End .copyrights -->
                <!-- Begin .app-download -->
                <div class="app-download">
                    <div class="qrcode-wrap">
                        <div class="qrcode"><img src="//st.jinfuzi.com/res/img/common/qrcode/app_jfz_caifu_float.png" alt=""></div>
                        <div class="text">扫描下载金斧子APP</div>
                    </div>
                </div>
                <!-- End .app-download -->
            </div>
            <!-- End .g-footer-main -->
        </div>
        <!-- End .container -->
    </div>
    <!-- End .g-footer -->

    <input id="force-login" type="hidden" value="1">






    		<div style="display: none;">
                <script>
                var _hmt = _hmt || [];
                (function() {
                  var hm = document.createElement("script");
                  hm.src = "https://hm.baidu.com/hm.js?9cfdc8c0bb3c0ab683956289eef9f34a";
                  var s = document.getElementsByTagName("script")[0];
                  s.parentNode.insertBefore(hm, s);
                })();
                //同步通栏跨域问题：
                function tranUrl(){
                    var url;
                    if(window.location.host.indexOf('jfz')>0) {
                        url = window.location.host.replace(/jfz/ig, 'jinfuzi');
                    }
                    if(window.location.host.indexOf('jinfuzi')>0){
                        url = window.location.host.replace(/jinfuzi/ig,'jfz');
                    }
                    return url;
                }
                </script>

                <script type="text/javascript">
                    require(['jquery','cookie'], function ($) {
                        var _vds= [];

                        _vds.push(['setAccountId', '9907c51ef09823c8d5b98c511e30a866']);

                        if(typeof $.cookie('jfz_login_id') != 'undefined' && $.cookie('jfz_login_id') != null)
                        {
                            _vds.push(['setCS1','user_id',$.cookie('jfz_login_id')]);
                            if(typeof $.cookie('jfz_user_type') != 'undefined' && $.cookie('jfz_user_type') != null)
                            {
                                _vds.push(['setCS2','usertype',$.cookie('jfz_user_type')]);
                            }
                        }
                        window._vds = _vds;
                        (function () {
                            var vds = document.createElement('script');
                            vds.type = 'text/javascript';
                            vds.async = !0;
                            vds.src = ('https:' == document.location.protocol ? 'https://' : 'http://') + 'dn-growing.qbox.me/vds.js';
                            var s = document.getElementsByTagName('script')[0];
                            s.parentNode.insertBefore(vds, s);
                        })();

                    })
                </script>

                <!-- Piwik -->
                <script type="text/javascript">
                    var _jfz_paq = _jfz_paq || [];
                    (function(){
                        _jfz_paq.push(['setSiteId', 1]);
                        _jfz_paq.push(['setTrackerUrl', 'https://tongji.jinfuzi.com/ClickStream.php']);
                        _jfz_paq.push(['setUserId',""]);
                        _jfz_paq.push(['setIpAddress','171.212.113.31']);
                    })();
                </script>

    		</div>
    			<script type="text/javascript" src="//st.jinfuzi.com/res/js/service/productCenter.js?v=2.4.1"></script>
    <script type="text/javascript" src="//st.jinfuzi.com/res/js/service/compare.js?v=2.4.1"></script>
    </body>
    </html><div class="uc_totop" id="back_totop" style="display: none;">
        <a href="javascript:;"></a>
    </div>


    """

    items = await FundItem.get_item(html=string)
    return items

if __name__ == '__main__':
    import asyncio
    asyncio.get_event_loop().run_until_complete(main())
