# -*- coding:utf8 -*-

import requests
import datetime
import time
import base64
import urllib
from urllib.parse import urlparse,parse_qs,unquote_plus
import rsa
import binascii
import math
import re
import json
import pickle
import sys
import os
from weibo_utils import logger,headers

COOKFILENAME='weibocookie.txt'
COOKFILENAMEPICKLE='weibocookie_pickle.txt'

def user_base64(user):
    userquote=urllib.parse.quote_plus(user)
    logger.debug('weibo user quote {}'.format( userquote ))
    userbase64 = base64.b64encode(user.encode('utf-8'))
    logger.debug('weibo user base64 {}'.format(userbase64.decode('utf-8')) )
    return userbase64.decode('utf-8')

def password_rsa(password, servertime, nonce, pubkey):

    rsaPublickey = rsa.PublicKey(int(pubkey,16), int('10001',16))
    # rsaPublickey = rsa.PublicKey(int(pubkey,16), 65537)
    message = str(servertime) + '\t' + str(nonce) + '\n' + password
    sp = rsa.encrypt(message.encode(), rsaPublickey)
    return binascii.b2a_hex(sp).decode('utf-8')

def weibo_http_get_raskey(user, session=None):
    '''
        returns the result on success or none on failure
    :param user: weibo login user name
    :return:
    '''
    url = "https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su={}&rsakt=mod&client=ssologin.js(v1.4.19)&_={}".format( user, str(int(time.time()*1000)) )
    logger.debug(url)

    try:
        headers['Referer'] = 'https://weibo.com/'
        if session:
            response = requests.get(url, headers=headers, verify=False)
        else:
            response = requests.get(url, headers=headers, verify=False)
        if response and response.status_code==200:
            logger.debug(response.content.decode('utf-8'))
            text = response.content.decode('utf-8')
            result = eval(text.replace('sinaSSOController.preloginCallBack',''))
            return result
            # nonce = re.findall(r'"nonce":"(.*?)"', text)[0]
            # pubkey = re.findall(r'"pubkey":"(.*?)"', text)[0]
            # rsakv = re.findall(r'"rsakv":"(.*?)"', text)[0]
            # servertime = re.findall(r'"servertime":(.*?),', text)[0]
        else:
            logger.error('request error http code:{}'.format(response.status_code))
            return None
    except Exception as e:
        logger.exception(sys.exc_info())
        return None

def weibo_http_get_verify_pic(pcid, session=None):
    '''
    download img files and return img file path
    :param pcid:
    :return: return img file path
    '''
    url = 'https://login.sina.com.cn/cgi/pin.php?r={}&s=0&p={}'.format( math.floor(random.random()*100000000), pcid )
    logger.debug(url)
    try:
        headers['Referer'] = 'https://weibo.com/'
        if session:
            response = session.get(url, headers=headers, verify=False)
        else:
            response = requests.get(url, headers=headers, verify=False)
        if response and response.status_code==200:
            filename = 'img/{}.png'.format(pcid)
            with open(filename, 'wb') as fp:
                fp.write(response.content)
            return filename
        else:
            logger.error('request error http code:{}'.format(response.status_code))
            return None
    except Exception as e:
        logger.exception(sys.exc_info())
        return None

def weibo_http_post_login_location(su, sp, nonce, rsakv, servertime, pcid=None, verify=None, session=None):
    url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
    logger.debug(url)

    try:
        # headers['Referer'] = 'https://weibo.com/'
        # headers.pop('Referer')
        datas={
            'entry':'weibo',
            'gateway':'1',
            'from':'',
            'savestate': '7',
            'qrcode_flag': 'false',
            'useticket': '1',
            'pagerefer':'https://login.sina.com.cn/crossdomain2.php?action=logout&r=https%3A%2F%2Fpassport.weibo.com%2Fwbsso%2Flogout%3Fr%3Dhttps%253A%252F%252Fweibo.com%26returntype%3D1',
            'vsnf': '1',
            'su': su,
            'service': 'miniblog',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode':'rsa2',
            'rsakv': rsakv,
            'sp':sp,
            'sr':'1366*768',
            'encoding':'UTF-8',
            'prelt':'115',
            'url':'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype':'META'
        }
        if verify:
            datas['pcid'] = pcid
            datas['door'] = verify
        logger.debug(datas)
        if session:
            response = session.post(url, headers=headers, data=datas, verify=False)
        else:
            response = requests.post(url, headers=headers, data=datas, verify=False)
        if response and response.status_code==200:
            txt = response.content.decode('gbk')
            logger.debug(txt)
            reGroups = re.match('.*location.replace\(\"(.*)\"\);.*', txt, re.S)
            locationDict = None
            if reGroups:
                locationUrl = reGroups.group(1)
                locationUrl = unquote_plus(locationUrl)
                logger.debug('unquote url {}'.format(locationUrl))

                locationDict = parse_qs(urlparse(locationUrl).query)

            return locationDict
        else:
            logger.error('request error http code:{}'.format(response.status_code))
            return None
    except Exception as e:
        logger.exception(sys.exc_info())
        return None

def weibo_http_get_home_uniqueid(ticket, ssosavestate, session=None):
    url = 'https://passport.weibo.com/wbsso/login?ticket={}&ssosavestate={}&callback=sinaSSOController.doCrossDomainCallBack&scriptId=ssoscript0&client=ssologin.js(v1.4.19)&_=1533119634900'.format(ticket, ssosavestate,str(int(time.time()*1000)) )
    logger.debug(url)

    try:
        # headers['Referer'] = 'https://weibo.com/'

        if session:
            response = session.get(url, headers=headers, verify=False)
        else:
            response = requests.get(url, headers=headers, verify=False)
        if response and response.status_code==200:
            txt = response.content.decode('gbk')
            logger.debug(txt)
            txt = txt.replace('sinaSSOController.doCrossDomainCallBack', '')
            txt = txt.replace(';', '')
            txt = txt.replace('true', '1')
            resultDict = eval(txt)
            return resultDict
        else:
            logger.error('request error http code:{}'.format(response.status_code))
            return None
    except Exception as e:
        logger.exception(sys.exc_info())
        return None

def weibo_http_get_home(uniqueid, session=None):
    url = 'https://weibo.com/u/{}/home?wvr=5&lf=reg'.format( uniqueid )
    logger.debug(url)

    try:
        headers['Referer'] = 'https://weibo.com/'
        if session:
            response = session.get(url, headers=headers, verify=False)
        else:
            response = requests.get(url, headers=headers, verify=False)
        if response and response.status_code==200:
            # txt = response.content.decode('utf8')
            # logger.debug(txt)
            return True
        else:
            logger.error('request error http code:{}'.format(response.status_code))
            return None
    except Exception as e:
        logger.exception(sys.exc_info())
        return None

def weibo_login(user, password, session=None):
    su = user_base64(user)
    preLoginDict = weibo_http_get_raskey(su, session=session)
    logger.debug('dict:{}'.format(preLoginDict))

    nonce = preLoginDict['nonce']
    pubkey = preLoginDict['pubkey']
    rsakv = preLoginDict['rsakv']
    servertime = preLoginDict['servertime']

    sp = password_rsa(password, servertime, nonce, pubkey)
    verify = None
    pcid = None
    if 'showpin' in preLoginDict.keys():
        pcid = preLoginDict['pcid']
        verify_file = weibo_http_get_verify_pic(pcid, session=session)
        # 验证码文件解析
        logger.error('verify file {}'.format(verify_file))
        verify = input("input verfy code:")

    locationParams = weibo_http_post_login_location(su, sp, nonce, rsakv, servertime, pcid, verify, session=session)
    if locationParams:
        retcode = locationParams['retcode'][0]
        ticket = locationParams['ticket'][0]
        rParams = parse_qs(urlparse(locationParams['r'][0]).query)
        ssosavestate = rParams['ssosavestate'][0]
    else:
        logger.error('weibo login error')
        return None

    resultDict = weibo_http_get_home_uniqueid(ticket, ssosavestate, session)

    if resultDict is None:
        logger.error('weibo login error')
        return None

    logger.debug("weibo login uniqueid {}".format(resultDict))
    uniqueid = resultDict['userinfo']['uniqueid']
    return weibo_http_get_home(uniqueid)

def weibo_login_cookie(user, password):
    session = requests.session()
    cookfile = '{}{}'.format(user,COOKFILENAME)
    if os.path.exists(cookfile):
        # os.stat  st_atime(访问时间), st_mtime(修改时间), st_ctime（创建时间）
        filestat = os.stat(cookfile)
        modifyDt = datetime.datetime.utcfromtimestamp(filestat.st_mtime).date()
        nowDt = datetime.datetime.now().date()
        print( modifyDt, nowDt)
        if modifyDt<nowDt:
            logger.debug('cookie file dated')
        else:
            cookieDict = {}
            with open(cookfile, 'r') as f:
                cookieDict = json.load(f)
            cookjar = requests.utils.cookiejar_from_dict(cookieDict)
            session.cookies = cookjar
            return session

    logining = weibo_login(user, password, session)

    if logining:
        # with open(COOKFILENAMEPICKLE, 'wb') as f:
        #     pickle.dump(session.cookies, f)
        cookies = requests.utils.dict_from_cookiejar(session.cookies)
        with open(cookfile, 'w') as f:
            f.write(json.dumps(cookies))

        return session
    else:
        return False


if __name__ == '__main__':
    user='18162758696'
    password='1111111'
    session = weibo_login_cookie(user, password)


