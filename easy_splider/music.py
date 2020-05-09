# -*- coding: utf8 -*-

'''
    问题：
        要代理访问或降低频率，容易访问被拒
        歌曲保存目录不全是歌手名字
        
    音乐网站音乐爬虫 http://music.taihe.com/
    完成目标：
            分布式
    分析过程：
    按歌手曲目页面       http://music.taihe.com/artist
    点击  薛之谦         http://music.taihe.com/artist/2517
    页面是音乐清单，可以提取音乐url             http://music.taihe.com/song/670310517
    js请求
    http://musicapi.taihe.com/v1/restserver/ting?method=baidu.ting.song.playAAC&format=jsonp&callback=jQuery172025913855760195204_1586009883033&songid=670310517&from=web&_=1586009898020
    js返回
    jQuery172025913855760195204_1586009883033({"songinfo":{"resource_type_ext":"0","si_presale_flag":"0","resource_type":"0","mv_provider":"0000000000","del_status":"0","collect_num":606,"hot":"60629","res_reward_flag":"0","sound_effect":"","title":"尘","language":"国语","play_type":0,"country":"内地","biaoshi":"first,lossless,perm-1","bitrate_fee":"{\"0\":\"0|0\",\"1\":\"0|0\"}","artist_1000_1000":"http:\/\/qukufile2.qianqian.com\/data2\/pic\/140d09665d1c204efe00973c3e16282c\/612757841\/612757841.jpg@s_2,w_1000,h_1000","is_first_publish":0,"artist_640_1136":"http:\/\/qukufile2.qianqian.com\/data2\/pic\/0578e11a9bdaa82223b67e2005edcd8c\/612757843\/612757843.jpg","charge":0,"copy_type":"1","share_url":"http:\/\/music.baidu.com\/play\/670310517","has_mv_mobile":0,"album_no":"1","is_charge":"","special_type":0,"has_filmtv":"0","pic_huge":"http:\/\/qukufile2.qianqian.com\/data2\/pic\/a8329896c66038ef4be51c67aa983c8f\/670312320\/670312320.jpg@s_2,w_1000,h_1000","ting_uid":"2517","expire":36000,"havehigh":2,"si_proxycompany":"华宇世博音乐文化（北京）有限公司-普通代理","compose":"薛之谦","toneid":"0","area":"0","info":"","artist_500_500":"http:\/\/qukufile2.qianqian.com\/data2\/pic\/140d09665d1c204efe00973c3e16282c\/612757841\/612757841.jpg@s_2,w_500,h_500","multiterminal_copytype":"","has_mv":0,"total_listen_nums":"446722","song_id":"670310517","piao_id":"0","high_rate":"320","artist":"薛之谦","artist_list":[{"avatar_mini":"http:\/\/qukufile2.qianqian.com\/data2\/pic\/140d09665d1c204efe00973c3e16282c\/612757841\/612757841.jpg@s_2,w_20,h_20","avatar_s300":"http:\/\/qukufile2.qianqian.com\/data2\/pic\/140d09665d1c204efe00973c3e16282c\/612757841\/612757841.jpg@s_2,w_300,h_300","ting_uid":"2517","del_status":"0","avatar_s500":"http:\/\/qukufile2.qianqian.com\/data2\/pic\/140d09665d1c204efe00973c3e16282c\/612757841\/612757841.jpg@s_2,w_500,h_500","artist_name":"薛之谦","avatar_small":"http:\/\/qukufile2.qianqian.com\/data2\/pic\/140d09665d1c204efe00973c3e16282c\/612757841\/612757841.jpg@s_2,w_48,h_48","avatar_s180":"http:\/\/qukufile2.qianqian.com\/data2\/pic\/140d09665d1c204efe00973c3e16282c\/612757841\/612757841.jpg@s_2,w_180,h_180","artist_id":"88"}],"comment_num":"0","compress_status":"0","original":0,"artist_480_800":"http:\/\/qukufile2.qianqian.com\/data2\/pic\/e1b3671f0c93c6fa03324436d2f9aebf\/612757842\/612757842.jpg","relate_status":"0","learn":0,"bitrate":"128,320","pic_big":"http:\/\/qukufile2.qianqian.com\/data2\/pic\/a8329896c66038ef4be51c67aa983c8f\/670312320\/670312320.jpg@s_2,w_150,h_150","album_1000_1000":"http:\/\/qukufile2.qianqian.com\/data2\/pic\/a8329896c66038ef4be51c67aa983c8f\/670312320\/670312320.jpg@s_2,w_1000,h_1000","pic_singer":"","songwriting":"薛之谦","album_500_500":"http:\/\/qukufile2.qianqian.com\/data2\/pic\/a8329896c66038ef4be51c67aa983c8f\/670312320\/670312320.jpg@s_2,w_500,h_500","song_source":"web","album_id":"670310515","share_num":19,"aliasname":"","artist_id":"88","korean_bb_song":"0","all_rate":"96,128,224,320,flac","author":"薛之谦","all_artist_id":"88","listen_nums":"816","publishtime":"2019-10-11","versions":"","all_artist_ting_uid":"2517","res_encryption_flag":"0","file_duration":"281","pic_radio":"http:\/\/qukufile2.qianqian.com\/data2\/pic\/a8329896c66038ef4be51c67aa983c8f\/670312320\/670312320.jpg@s_2,w_300,h_300","distribution":"0000000000,0000000000,0000000000,0000000000,0000000000,0000000000,0000000000,0000000000,0000000000,0000000000","lrclink":"http:\/\/qukufile2.qianqian.com\/data2\/lrc\/20d88393cecfd39f7887a1cd7fd05856\/670310591\/670310591.lrc","pic_small":"http:\/\/qukufile2.qianqian.com\/data2\/pic\/a8329896c66038ef4be51c67aa983c8f\/670312320\/670312320.jpg@s_2,w_90,h_90","album_title":"尘","original_rate":"","pic_premium":"http:\/\/qukufile2.qianqian.com\/data2\/pic\/a8329896c66038ef4be51c67aa983c8f\/670312320\/670312320.jpg@s_2,w_500,h_500"},"error_code":22000,"bitrate":{"show_link":"http:\/\/audio04.dmhmusic.com\/71_53_T10052050224_128_4_1_0_sdk-cpm\/cn\/0209\/M00\/D1\/D6\/ChR4612fBfKAIxmwAETDbyjcp2A545.mp3?xcode=b0bf149ec7f4cde0620c6063e091514f44d8900","free":1,"replay_gain":"0.000000","song_file_id":0,"file_size":4506479,"file_extension":"mp3","file_duration":281,"file_format":"mp3","file_bitrate":128,"file_link":"http:\/\/audio04.dmhmusic.com\/71_53_T10052050224_128_4_1_0_sdk-cpm\/cn\/0209\/M00\/D1\/D6\/ChR4612fBfKAIxmwAETDbyjcp2A545.mp3?xcode=b0bf149ec7f4cde0620c6063e091514f44d8900","original":0}});
    音乐地址
    http://audio04.dmhmusic.com/71_53_T10052050224_128_4_1_0_sdk-cpm/cn/0209/M00/D1/D6/ChR4612fBfKAIxmwAETDbyjcp2A545.mp3?xcode=b0bf149ec7f4cde0620c6063e091514f44d8900

    js参数：songid 是 音乐url后的数字670310517  jQuery值(未知规则)17204780742719340729_1586053549318    _值(未知规则)1586053553445
    http://musicapi.taihe.com/v1/restserver/ting?method=baidu.ting.song.playAAC&format=jsonp&callback=jQuery{}&songid={}&from=web&_={}
'''
import requests
import random
import logging
import json
import hashlib
import time
import urllib.parse
import os
import sys
import datetime
import re
from concurrent.futures import ThreadPoolExecutor,as_completed
from bs4 import BeautifulSoup
from queue import PriorityQueue
from inspect import isgeneratorfunction
from music_models import MediaInfo, RequestInfo, ArtistInfo, request_info_update_insert, dbsession
from weibo_utils import headers,logger,requestQueue


'''
    (priority,RequestInfo, parm)
    RequestInfo requestName调用的函数名
                requestUrl调用的url  参数1
'''

PRIORITYDEFINE={
    'get_media_info_js_request':2,
    'down_media_file':1,
    'get_artist_music_list_xhr':3,
    'get_artist_music_list':4
}

def request_variable_init(url, requestInfo=None):
    if requestInfo is None:
        requestInfo = RequestInfo()
        requestInfo.runCnt = 1
    else:
        if requestInfo.runCnt is None:
            requestInfo.runCnt = 0
        requestInfo.runCnt = requestInfo.runCnt + 1

    requestInfo.requestUrl = url
    md5 = hashlib.md5()
    md5.update(url.encode('utf-8'))
    requestInfo.urlId = md5.hexdigest()
    requestInfo.status = 999
    requestInfo.requestDate = datetime.date.today()
    requestInfo.requestTime = datetime.datetime.now().time()

    return requestInfo

def get_media_info_js_request(url):
    logger.debug('request url {}'.format(url))

    requestInfo = request_variable_init(url)
    requestInfo.requestName = 'get_media_info_js_request'

    headers['Referer'] = url
    httpSession = requests.session()
    s_time = time.time()
    mediaInfo = None
    try:
        response = httpSession.get(url, headers=headers)

        if response and response.status_code==200:
            requestInfo.status = response.status_code
            # jsonStr = response.text.strip('jQuery{}('.format(jQuery))
            # jsonStr = jsonStr.strip(');')
            pattern = re.compile('^jQuery\S*\(({.*})\);$')
            reGroups = pattern.match(response.text)
            if reGroups:
                jsonStr = reGroups.group(1)
            else:
                requestInfo.status = 0
                logger.error('parser js none')
                return requestInfo, None

            jsonObj = json.loads(jsonStr)

            mediaInfo = MediaInfo()
            mediaInfo.mediaUrl = jsonObj['bitrate']['show_link']
            md5 = hashlib.md5()
            md5.update(mediaInfo.mediaUrl.encode('utf-8'))
            mediaInfo.mediaId = md5.hexdigest()

            ###ERROR 检查必要字段是否为空 为空特别处理

            mediaInfo.mediaName = jsonObj['songinfo']['title']
            mediaInfo.mediaLang =  jsonObj['songinfo']['language']
            mediaInfo.country = jsonObj['songinfo']['country']
            mediaInfo.proxycompany = jsonObj['songinfo']['si_proxycompany']
            mediaInfo.compose = jsonObj['songinfo']['compose']
            mediaInfo.writer = jsonObj['songinfo']['songwriting']
            mediaInfo.author = jsonObj['songinfo']['author']
            mediaInfo.publishTime = jsonObj['songinfo']['publishtime']
            mediaInfo.albumName = jsonObj['songinfo']['album_title']
            mediaInfo.lrcUrl = jsonObj['songinfo']['lrclink']
            mediaInfo.mediaSize = jsonObj['bitrate']['file_size']
            mediaInfo.mediaFormat = jsonObj['bitrate']['file_format']
            mediaInfo.albumId = jsonObj['songinfo']['album_id']
            # 1 版权原因删除  0正常可听
            mediaInfo.useStatus = jsonObj['songinfo']['del_status']

            mediaInfo.source = urllib.parse.urlparse(mediaInfo.mediaUrl).netloc
            # mediaInfo.sourceDate = time.strftime('%Y%m%d', time.localtime(time.time()))
            e_time = time.time()
            mediaInfo.useTime = e_time-s_time
            logger.debug('media url {}'.format(mediaInfo.mediaUrl))

            requestInfo = request_variable_init(mediaInfo.mediaUrl)
            requestInfo.requestName = 'down_media_file'

        else:
            logger.error('requests error {}'.format(response if response is None else response.status_code))
            requestInfo.status = response.status_code if response else 0

    except requests.exceptions.ConnectTimeout as e:
        # 连接超时  服务器在指定时间内没有应答
        requestInfo.status = -3
        logger.exception(sys.exc_info())
    except requests.exceptions.ReadTimeout as e:
        # 读取超时 客户端等待服务器发送第一个字节之前的时间
        requestInfo.status = -3
        logger.exception(sys.exc_info())
    except requests.exceptions.ConnectionError as e:
        # 网络环境异常 或 服务器异常
        requestInfo.status = -2
        logger.exception(sys.exc_info())
    except requests.exceptions.RequestException as e:
        requestInfo.status = -1
        logger.exception(sys.exc_info())
    except Exception as e:
        logger.exception(sys.exc_info())
        requestInfo.status = 0
        return requestInfo, None

    return requestInfo, mediaInfo

def down_media_file(url, mediaInfo=None):
    baseDir = "song"

    requestInfo = request_variable_init(url)
    requestInfo.requestName = 'down_media_file'

    if mediaInfo:
        headers['Referer'] = url

        # 判断下载文件、目录是否已存在
        addr = '{}/{}'.format(baseDir, mediaInfo.author)
        if not os.path.exists(addr):
            os.mkdir(addr)
        addr = os.path.join(addr, '{}.{}'.format(mediaInfo.mediaName, mediaInfo.mediaFormat))
        logger.debug('media addr {}'.format(addr))
    else:
        md5 = hashlib.md5()
        md5.update(url.encode('utf-8'))
        addr =  os.path.join(baseDir, md5.hexdigest())
        logger.debug('media addr {}'.format(addr))

    if os.path.exists(addr):
        logger.debug('media addr {} is exists'.format(addr))
        requestInfo.status = 0
        return requestInfo,None

    try:
        logger.debug('request url {}'.format(url))
        response = requests.get(url, headers=headers)
    except requests.exceptions.ConnectTimeout as e:
        # 连接超时  服务器在指定时间内没有应答
        requestInfo.status = -3
        logger.exception(sys.exc_info())
    except requests.exceptions.ReadTimeout as e:
        # 读取超时 客户端等待服务器发送第一个字节之前的时间
        requestInfo.status = -3
        logger.exception(sys.exc_info())
    except requests.exceptions.ConnectionError as e:
        # 网络环境异常 或 服务器异常
        requestInfo.status = -2
        logger.exception(sys.exc_info())
    except requests.exceptions.RequestException as e:
        requestInfo.status = -1
        logger.exception(sys.exc_info())
    except Exception as e:
        logger.exception(sys.exc_info())
        requestInfo.status = 0

    if response and response.status_code==200:
        requestInfo.status = response.status_code
        try:
            with open(addr, 'wb') as fp:
                fp.write(response.content)
        except Exception as e:
            requestInfo.status = 0
            logger.exception(sys.exc_info())
    else:
        logger.error('requests error {}'.format(response if response is None else response.status_code))
        requestInfo.status = response.status_code if response else 0
    return requestInfo,None

###discard function
def get_media_workflow(songid):
    # 正常流程
    jQuery = '17204780742719340729_1586053549318'
    item = '1586053553445'
    url = 'http://musicapi.taihe.com/v1/restserver/ting?method=baidu.ting.song.playAAC&format=jsonp&callback=jQuery{}&songid={}&from=web&_={}'.format(jQuery,songid,item)

    requestInfo,info = get_media_info_js_request(url)

    #成功获取媒体信息
    if info:
        #请求信息入库
        dbsession.add(requestInfo)
        # 媒体信息入库
        dbsession.add(info)

        s_time = time.time()
        requestInfo,result = down_media_file(info.mediaUrl, info)
        e_time = time.time()

        # 更新媒体信息 下载状态 下载用时
        info.downStatus = '00'
        info.downTime = e_time - s_time

        if requestInfo and requestInfo.status == 200:
            # 请求信息入库
            dbsession.add(requestInfo)
        else:
            # 判断哪些请求入库 哪些请求信息入队列
            if requestInfo.status == 0:
                dbsession.add(requestInfo)
            if requestInfo.status<0 and (requestInfo.runCnt + requestInfo.status)>0:
                dbsession.add(requestInfo)
            else:
                requestQueue.put([requestInfo.status,requestInfo])
    else:
        # print(requestInfo.status, requestInfo.runCnt)
        if requestInfo and requestInfo.status == 0:
            dbsession.add(requestInfo)
        if requestInfo and requestInfo.status < 0 and (requestInfo.runCnt + requestInfo.status) > 0:
            dbsession.add(requestInfo)
        else:
            requestQueue.put([requestInfo.status, requestInfo])
            logger.debug('requestQueue size {}'.format(requestQueue.qsize()))

    try:
        dbsession.commit()
    except Exception as e:
        dbsession.rollback()
        logger.exception(sys.exc_info())

def get_artist_music_list_xhr(url):
    headers['Referer'] = url

    try:
        logger.debug('request url {}'.format(url))

        requestInfo = request_variable_init(url)
        requestInfo.requestName = 'get_artist_music_list_xhr'

        response = requests.get(url, headers=headers)

        if response and response.status_code == 200:
            requestInfo.status = response.status_code
            jsonObj = json.loads(response.content.decode('utf8'))
            htmlText = jsonObj['data']['html']
            # logger.debug(htmlText)

            # htmlText = html.unescape(htmlText)
            # logger.debug(htmlText)

            # htmlText = htmlText.encode('utf8').decode('unicode-escape')
            # logger.debug(htmlText)

            # text = response.content.decode('unicode-escape')
            # import html
            # text = html.unescape(text)

            # r'<a href="/song/(\d+)" target="_blank" class="namelink" title="(.*)" a-tj'
            pattern = re.compile("<a href=\"/song/(\d+)\" target=\"_blank\" class=\"namelink \w*\" title=\"(\S*)\" a-tj", re.S)
            reGroups = pattern.findall(htmlText)

            if reGroups:
                jQuery = '17204780742719340729_1586053549318'
                item = '1586053553445'
                for songid,k in reGroups:
                    # print(i,k)
                    url = 'http://musicapi.taihe.com/v1/restserver/ting?method=baidu.ting.song.playAAC&format=jsonp&callback=jQuery{}&songid={}&from=web&_={}'.format(jQuery, songid, item)
                    resultInfo = request_variable_init(url)
                    resultInfo.requestName = 'get_media_info_js_request'
                    yield  resultInfo,None
            else:
                requestInfo.status = 0
                logger.error('parser music list xr error')
        else:
            requestInfo.status = response.status_code if response else 0
            logger.error('requests error {}'.format(response if response is None else response.status_code))

    except Exception as e:
        logger.exception(sys.exc_info())
    yield requestInfo, None

'''
歌手页面歌曲清单
    例:http://music.taihe.com/artist/2517
    获取歌曲id
'''
def get_artist_music_list(url):

    headers['Referer'] = url
    try:
        logger.debug('request url {}'.format(url))
        requestInfo = request_variable_init(url)
        requestInfo.requestName = 'get_artist_music_list'
        response = requests.get(url, headers=headers)

        if response and response.status_code==200:
            requestInfo.status = response.status_code
            # soup = BeautifulSoup(response.content.decode('utf8'), 'html5lib')
            # tag = soup.find('div',class_='page_navigator-box').find('div', class_='page-navigator-hook')
            # if tag:
            #     attr = tag['class']
            #     print(attr)
            #     total = attr[5].strip(',').split(':')[1]
            #     size = attr[6].strip(',').split(':')[1]
            #     print(total, size)

            # pattern = re.compile(".*'total':(\d+),[ \t]*'size':(\d+).*", re.S)
            pattern = re.compile("'total':(\d+),[ \t]*'size':(\d+)", re.S)
            totalGroup = pattern.findall(response.content.decode('utf8'))

            if totalGroup:
                # 0歌曲 1专辑 2视屏
                total = int(totalGroup[0][0].strip("'"))
                size = int(totalGroup[0][1].strip("'"))

                ting_uid = url[url.rindex('/')+1:]
                for i in range(0, total, size):
                    # 获取歌曲总数 每次调用xhr获取歌曲数量
                    xhrUrl = 'http://music.taihe.com/data/user/getsongs?start={}&size={}&ting_uid={}&r=0.196355769444312541586235172159'.format(i,size,ting_uid)
                    # get_artist_music_list_xhr(xhrUrl)

                    resultInfo = request_variable_init(xhrUrl)
                    resultInfo.requestName = 'get_artist_music_list_xhr'
                    yield  resultInfo,None
            else:
                requestInfo.status = 0
                logger.error('parser music list none')
        else:
            requestInfo.status = response.status_code if response else 0
            logger.error('requests error {}'.format( response if response is None else response.status_code))
    except Exception as e:
        requestInfo.status = 0
        logger.exception(sys.exc_info())

    yield requestInfo,None

#pass
def get_artist_info(url):
    # http://music.taihe.com/data/tingapi/v1/restserver/ting?method=baidu.ting.artist.getInfo&from=web&tinguid=1097
    headers['Referer'] = url

    try:
        logger.debug('request url {}'.format(url))
        response = requests.get(url, headers=headers)

        if response and response.status_code == 200:
            pass
        else:
            logger.error('requests error {}'.format(response if response is None else response.status_code))
    except Exception as e:
        logger.exception(sys.exc_info())

'''
歌手清单
    例:http://music.taihe.com/artist
    获取歌手id
    歌手数不多，生成dict
'''
def get_artist_list(url, filename=None):
    headers['Referer'] = url

    artistDict = {}

    #从json文件导出歌手清单
    if filename and os.path.exists(filename) and os.path.getsize(filename)>0:
        # print(os.stat(filename).st_ctime,os.stat(filename).st_mtime)
        try:
            with open(filename, 'r', encoding='utf8') as fp:
                artistDict = json.load(fp)

            return artistDict
        except Exception as e:
            logger.exception(sys.exc_info())
            raise

    try:
        logger.debug('request url {}'.format(url))
        response = requests.get(url, headers=headers)

        if response and response.status_code == 200:
            soup = BeautifulSoup(response.content.decode('utf8'), 'html5lib')

            musicBodyTag = soup.find('div', class_='music-body clearfix').find('div', class_='main-body').find('ul', class_='container')
            if musicBodyTag:
                musicTagList = musicBodyTag.find_all('a',{'href':re.compile("^.*/[0-9]*$"), 'title':re.compile("^.*$")})
                for tag in musicTagList:
                    artist = tag['title']
                    id = tag['href'][8:]
                    artistDict[id] = artist
            else:
                logger.error('parser artist list none')
        else:
            logger.error('requests error {}'.format(response if response is None else response.status_code))

    except Exception as e:
        logger.exception(sys.exc_info())
        return None

    if filename:
        try:
            with open(filename, 'w', encoding='utf8') as fp:
                json.dump(artistDict, fp, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.exception(sys.exc_info())
            raise
    return artistDict


def request_workflow_thread():
    while True:
        try:
            priority,requestInfo,param = requestQueue.get(block=True, timeout=10)
            requestQueue.task_done()
            logger.debug('PriorityQueue size {}'.format(requestQueue.qsize()))
        except Exception as e:
            logger.exception(sys.exc_info())
            logger.error('request_workflow_thread queue empty')
            break

        if requestInfo and requestInfo.requestName:
            logger.debug('run {} params {}'.format(requestInfo.requestName,requestInfo.requestUrl))
            if requestInfo.requestName == 'down_media_file':
                results = eval(requestInfo.requestName)(requestInfo.requestUrl,param)
            else:
                results=eval(requestInfo.requestName)(requestInfo.requestUrl)
            if isgeneratorfunction(eval(requestInfo.requestName)):
                logger.debug('isgeneratorfunction {} true'.format(requestInfo.requestName))
                for resultInfo,result in results:
                    if resultInfo.status == 999:
                        logger.debug('PriorityQueue put {},{} '.format(resultInfo.requestName,resultInfo.requestUrl))
                        requestQueue.put((PRIORITYDEFINE[resultInfo.requestName],resultInfo,result))
                    else:
                        if isinstance(result, MediaInfo) or isinstance(result, MediaInfo) or isinstance(result, ArtistInfo):
                            dbsession.add(result)
                    request_info_update_insert(requestInfo)
                    try:
                        dbsession.commit()
                    except Exception as e:
                        logger.exception(sys.exc_info())
                        logger.error('dbsession error')
                        dbsession.rollback()
            else:
                logger.debug('isgeneratorfunction {} false'.format(requestInfo.requestName))
                resultInfo, result = results

                if isinstance(result, MediaInfo) or isinstance(result, MediaInfo) or isinstance(result, ArtistInfo):
                    dbsession.add(result)

                request_info_update_insert(requestInfo)
                if resultInfo.status != 999:
                    logger.debug('dbsession add resultInfo {}'.format(resultInfo.urlId))
                else:
                    logger.debug('PriorityQueue put {},{} '.format(resultInfo.requestName, resultInfo.requestUrl))
                    requestQueue.put((PRIORITYDEFINE[resultInfo.requestName],resultInfo,result))

                try:
                    dbsession.commit()
                except Exception as e:
                    logger.exception(sys.exc_info())
                    logger.error('dbsession error')
                    dbsession.rollback()

        else:
            logger.error('request_workflow_thread requestInfo none')
            break

def scrapy_work():
    threadObjs = []
    max_workers = 5
    threadPool = ThreadPoolExecutor(max_workers=max_workers)
    for i in range(max_workers):
        obj=threadPool.submit(request_workflow_thread)
        threadObjs.append(obj)

    requestQueue.join()
    for _ in as_completed(threadObjs):
        logger.debug('one thread over')


    #error result, the main thread over but threads not over
    # while True:
    #     theadFlag = False
    #     for obj in threadObjs:
    #         theadFlag = theadFlag or obj.done()
    #
    #     if theadFlag:
    #         for obj in threadObjs:
    #             if obj.done():
    #                 threadObjs.remove(obj)
    #                 obj=threadPool.submit(request_workflow_thread)
    #                 threadObjs.append(obj)
    #     else:
    #         logger.debug('all threads over')
    #         break

    logger.debug('main threads over')

def test_down_media_file():
    url='http://audio04.dmhmusic.com/71_53_T10040589078_128_4_1_0_sdk-cpm/cn/0206/M00/90/77/ChR47F1_nqiAfD0hAD_MGBybIdk026.mp3?xcode=5d3eb51120589421625bfef5e4dc35bbc5db9a6'
    down_media_file(url)

def test_get_artist_list():
    artistDict = get_artist_list('http://music.taihe.com/artist', r'D:\project\python\pylib\artistjson.txt')

def test_get_artist_music_list_xhr():
    result = get_artist_music_list_xhr('http://music.taihe.com/data/user/getsongs?start=780&size=15&ting_uid=1097&r=0.196355769444312541586235172159')
    if isgeneratorfunction(get_artist_music_list_xhr):
        for i,k in result:
            print(i.requestUrl,i.status,type(k))

def test_get_artist_music_list():
    url = 'http://music.taihe.com/artist/1097'
    result = get_artist_music_list(url)
    print(type(result))
    for i,k in result:
        print(i.requestUrl,type(k))
    result = get_artist_music_list_xhr('http://music.taihe.com/data/user/getsongs?start=780&size=15&ting_uid=1097&r=0.196355769444312541586235172159')
    if isgeneratorfunction(get_artist_music_list_xhr):
        for i,k in result:
            print(i.requestUrl,i.status,type(k))

def test_get_media_workflow():
    get_media_workflow('670310517')

def test_scrapy_work():
    artistDict = get_artist_list('http://music.taihe.com/artist', r'D:\project\python\pylib\artistjson.txt')

    # print(artistDict)
    # for k,v in artistDict.items():
    #     url = 'http://music.taihe.com/artist/{}'.format(k)
    #     requestInfo = request_variable_init(url)
    #     requestInfo.requestName = 'get_artist_music_list'
    #     print(url,v)
    #     requestQueue.put((PRIORITYDEFINE[requestInfo.requestName],requestInfo))

    url = 'http://music.taihe.com/artist/{}'.format('2517')
    requestInfo = request_variable_init(url)
    requestInfo.requestName = 'get_artist_music_list'
    requestQueue.put((PRIORITYDEFINE[requestInfo.requestName], requestInfo, None))

    scrapy_work()


def test():
    # test_down_media_file()
    test_scrapy_work()
    # get_media_workflow('670310517')

def init_work():
    result = dbsession.query(RequestInfo).first()
    if result is None:
        artistDict = get_artist_list('http://music.taihe.com/artist', r'D:\project\python\pylib\artistjson.txt')

        for k, v in artistDict.items():
            url = 'http://music.taihe.com/artist/{}'.format(k)
            requestInfo = request_variable_init(url)
            requestInfo.requestName = 'get_artist_music_list'
            requestQueue.put((PRIORITYDEFINE[requestInfo.requestName], requestInfo, None))

        print(requestQueue.qsize())
    else:
        logger.debug('scrapy reboot from db')
        infos = dbsession.query(RequestInfo).filter_by( status = '999').all()
        for item in infos:
            logger.debug('scrapy reboot from db {}'.format(item))
            requestQueue.put((1, item, None))

def main():
    init_work()
    scrapy_work()

if __name__ == '__main__':
    # test()
    main()
