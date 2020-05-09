# -*- coding: utf-8 -*-
import requests
import sys
import re
import json
import os
from weibo_utils import logger,headers,request_variable_init
from weibo_models import WeiboUser

def weibo_http_get_tophot_list(session=None):
    '''
        return to the list of hot searches
    :param session:
    :return: returns like [(url,topname),(url,topname)] on success and None on failure
    '''
    url = 'https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6'
    logger.debug(url)

    try:
        headers['Referer'] = 'https://weibo.com/'
        if session:
            response = session.get(url, headers=headers, verify=False)
        else:
            response = requests.get(url, headers=headers, verify=False)

        if response and response.status_code==200:
            txt = response.content.decode('utf8')
            logger.debug(txt)
            # pattern = re.compile(r'<td class="td-02">\s*<a href="(.*)" target="_blank">(.*)</a>.*</td>',re.S)
            pattern = re.compile(r'<td class="td-02">\s*?<a href="(.*?)" target="_blank">(\S*?)</a>.*?</td>', re.S)
            reGroups = pattern.findall(txt)
            if reGroups:
                return None
            return reGroups
        else:
            logger.error('request error http code:{}'.format(response.status_code))
            return None
    except Exception as e:
        logger.exception(sys.exc_info())
        return None

def weibo_http_get_navigation_page_list(url,session=None):
    '''
        获取导航页各分类标签地址
    :param session:
    :return:
    '''
    logger.debug(url)
    try:
        headers['Referer'] = 'https://weibo.com/'
        requestInfo = request_variable_init(url)
        requestInfo.requestName = 'weibo_http_get_navigation_page_list'

        if session:
            response = session.get(url, headers=headers, verify=False)
        else:
            response = requests.get(url, headers=headers, verify=False)

        if response and response.status_code==200:
            requestInfo.status = response.status_code
            txt = response.content.decode('utf-8')
            # logger.debug(txt)
            # 查找匹配默认是贪婪法则 加上?号后转为非贪婪
            pattern = re.compile(r'<li class=\\"li_1 clearfix\\">(.*?)<\\/li>', re.S)
            reGroups = pattern.findall(txt)
            if not reGroups:
                logger.error('re find li_1 clearfix error')
                yield requestInfo, None
            else:
                navigationDict = {}
                for item in reGroups:
                    pattern = re.compile(r'<span class=\\"pt_title S_txt2\\">(.*?)<\\/span>', re.S)
                    reTags = pattern.findall(item)
                    key = reTags[0].replace('：','')
                    pattern = re.compile(r'<a target=\\"_blank\\" href=\\"(.*?)\\".*?<span.*?<\\/span>(.*?)<\\/a>', re.S)
                    reTags = pattern.findall(item)
                    value = [(v[0],v[1].replace('\\t','').strip()) for v in reTags]
                    id,name = value[0]
                    id = id[:id.rindex('_')]+'_0'
                    name='全部'
                    value.insert(0,(id,name))
                    navigationDict[key] = value

                    url = 'https://d.weibo.com/{}#'.format( id )
                    resultInfo = request_variable_init(url)
                    resultInfo.requestName = 'weibo_http_get_navigation_page_url'
                    yield resultInfo, None
            # logger.debug(navigationDict)
        else:
            logger.error('request error http code:{}'.format(response.status_code))
            requestInfo.status = response.status_code if response else 0
    except Exception as e:
        logger.exception(sys.exc_info())
        requestInfo.status = 0

    yield requestInfo, None

def weibo_http_get_navigation_page_url(url, session=None):
    '''
        通过分类标签页获取当前分类标签下所有数据url
    :param url:
    :param session:
    :return:
    '''
    try:
        headers['Referer'] = 'https://weibo.com/'
        logger.debug('request url {}'.format(url))
        requestInfo = request_variable_init(url)
        requestInfo.requestName = 'weibo_http_get_navigation_page_url'

        if session:
            response = session.get(url, headers=headers, verify=False)
        else:
            response = requests.get(url, headers=headers, verify=False)

        if response and response.status_code==200:
            requestInfo.status = response.status_code
            txt = response.content.decode('utf-8')
            # logger.debug(txt)
            # 查找匹配默认是贪婪法则 加上?号后转为非贪婪
            pattern = re.compile(r'<div class=\\"W_pages\\">(.*?)<\\/div>', re.S)
            reGroups = pattern.findall(txt)
            if not reGroups:
                logger.error('re find li_1 clearfix error')
                yield requestInfo, None
            if reGroups:
                allPagesTxt = reGroups[0]
                pattern = re.compile(r'href=\\"\\(.*?)\\">', re.S)
                reGroups = pattern.findall(allPagesTxt)

                maxPageTxt = reGroups[-2]
                logger.debug( maxPageTxt )
                maxPageReGroups = re.search(r'&page=(\d*)', maxPageTxt)
                maxPage = int(maxPageReGroups.group(1))
                logger.debug( maxPageReGroups.group(1) )
                strFormat = maxPageTxt.replace('page={}'.format(maxPage),'page={}')
                logger.debug(strFormat)

                for i in range(1, maxPage+1):
                    url = strFormat.format(i)
                    url = 'https://d.weibo.com{}'.format(url)
                    logger.debug(url)
                    resultInfo = request_variable_init(url)
                    resultInfo.requestName = 'weibo_http_get_navigation'
                    yield resultInfo, None
        else:
            logger.error('request error http code:{}'.format(response.status_code))
            requestInfo.status = response.status_code if response else 0
    except Exception as e:
        logger.exception(sys.exc_info())
        requestInfo.status = 0

    yield requestInfo, None

def weibo_http_get_navigation(url, session=None):
    '''
        获取账户信息
    :param url:
    :param session:
    :return:
    '''
    try:
        headers['Referer'] = 'https://weibo.com/'
        logger.debug('request url {}'.format(url))
        requestInfo = request_variable_init(url)
        requestInfo.requestName = 'weibo_http_get_navigation'

        if session:
            response = session.get(url, headers=headers, verify=False)
        else:
            response = requests.get(url, headers=headers, verify=False)

        if response and response.status_code==200:
            requestInfo.status = response.status_code
            txt = response.content.decode('utf-8')
            pattern = re.compile(r'<li class=\\"follow_item S_line2\\">(.*?)<\\/li>', re.S)
            reGroups = pattern.findall(txt)
            if not reGroups:
                logger.error('re find li_1 clearfix error')
                return requestInfo, None
            else:
                logger.debug(reGroups)
                userList = []
                for item in reGroups:
                    user = WeiboUser()
                    # 头像
                    pattern = re.compile(r'<dt class=\\"mod_pic\\">.*?src=\\"(.*?)\\".*<\\/dt>', re.S)
                    picReGroups = pattern.findall(item)
                    # print(picReGroups)

                    # 名称
                    # '<strong.*?usercard=\\"(.*?)\\"\s*>(.*?)<\\/strong>.*?<i.*?class=\\"(.*?)\\".*?><\\/i>.*?'
                    pattern = re.compile(
                        r'<div class=\\"info_name W_fb W_f14\\">(.*?)<\\/div>',
                        re.S)
                    infoNameGroups = pattern.findall(item)
                    if infoNameGroups:
                        txt = infoNameGroups[0]
                        tags = re.findall(r'.*<strong.*?usercard=\\"(.*?)\\"\s*>(.*?)<\\/strong>.*', txt, re.S)
                        if tags:
                            user.username = tags[0][1]
                            user.userid = tags[0][0]
                        tags = re.findall(r'<i.*?class=\\"(.*?)\\".*?><\\/i>', txt, re.S)
                        if tags:
                            for tag in tags:
                                if 'icon_approve' in tag:
                                    # 微博个人认证
                                    user.verify = '1'
                                elif 'icon_female' in tag:
                                    user.gender='female'
                                elif 'icon_male' in tag:
                                    user.gender = 'male'
                                elif 'icon_member' in tag:
                                    # 微博会员
                                    user.member = '1'

                    # 关注情况
                    pattern = re.compile(r'<div class=\\"info_connect\\">.*?<em class=\\"count\\">(.*?)<\\/em>.*?<em class=\\"count\\">(.*?)<\\/em>.*?<em class=\\"count\\">(.*?)<\\/em>.*?<\\/div>', re.S)
                    infoConnectGroups = pattern.findall(item)
                    user.focusnumber, user.fansnumber, user.weibonumber = infoConnectGroups[0]
                    # user.focusnumber = int(infoNameGroups[0][0])
                    # user.fansnumber = int(infoNameGroups[0][1])
                    # user.weibonumber = int(infoNameGroups[0][2])

                    # 地址
                    pattern = re.compile(r'<div class=\\"info_add\\">.*?<span>(.*?)<\\/span>.*?<\\/div>', re.S)
                    infoAddGroups = pattern.findall(item)
                    adds = infoAddGroups[0].split(' ')
                    # print(infoAddGroups, adds)
                    if len(adds)==2:
                        user.province = adds[0]
                        user.city = adds[1]
                    else:
                        user.province = adds[0]
                        user.city = adds[0]

                    # 简介
                    pattern = re.compile(r'<div class=\\"info_intro\\">.*?<span>(.*?)<\\/span>.*?<\\/div>', re.S)
                    infoIntroGroups = pattern.findall(item)
                    user.intro = infoIntroGroups[0]
                    # print(user.intro)
                    userList.append(user)

                return requestInfo, userList
        else:
            logger.error('request error http code:{}'.format(response.status_code))
            requestInfo.status = response.status_code if response else 0
    except Exception as e:
        logger.exception(sys.exc_info())
        requestInfo.status = 0

    return requestInfo, None



#


if __name__=='__main__':
    txt = '''https://d.weibo.com/1087030002_2975_5001_30'''
    print(txt[:txt.rindex('_')])
    pass