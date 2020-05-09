# -*- coding: utf-8 -*-
import requests
import sys
from bs4 import BeautifulSoup
import hashlib
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor,as_completed
from inspect import isgeneratorfunction
from weibo_utils import headers,logger,requestQueue,request_variable_init
from models import *

# 不设职位搜索条件
keyword = '%2520'

PRIORITYDEFINE={
    'job51_http_get_city_code':60,
    'job51_http_get_page_total':40,
    'job51_http_get_job_list':20,
    'job51_http_get_job_info':10
}

#获取城市的城市编号
def job51_http_get_city_code( url ):
    '''
    json    load loads
            dump dumps
    :param filename:
    :return:
    '''

    try:
        headers['Referer'] = url
        requestInfo = request_variable_init(url)
        requestInfo.requestName = 'job51_http_get_city_code'

        response = requests.get(url, headers=headers, verify=False)
        if response and response.status_code == 200:
            requestInfo.status = response.status_code

            text = response.text
            i = text.index('window.area')
            j = text.index('}', i)

            area = text[i:j]
            area = area.replace('window.area={', '')

            areaList = area.split(',')
            cityDict = {}

            for item in areaList:
                city = item.split(':')
                cityDict[city[1].strip('\"\t\n')] = city[0].strip('\"\t\n')

            for k,v in cityDict.items():
                url = 'https://search.51job.com/list/' + str(v) + ',000000,0000,00,9,99,' + keyword + ',2,1.html'
                logger.debug(url)
                resultInfo = request_variable_init(url)
                resultInfo.requestName = 'job51_http_get_page_total'
                yield resultInfo, None
        else:
            logger.error('request error http code:{}'.format(response.status_code))
            requestInfo.status = response.status_code if response else 0
    except Exception as e:
        # logger.exception(sys.exc_info())
        logger.error('error')
        requestInfo.status = 0

    yield requestInfo,None

def job51_http_get_page_total( url ):
    '''
    #获取职位总页数
    :param city_code: 地市编号
    :param keyword: 职位关键字
    :return:
    '''

    try:
        # headers['Referer'] = url
        requestInfo = request_variable_init(url)
        requestInfo.requestName = 'job51_http_get_page_total'
        logger.debug(url)
        response = requests.get(url, headers=headers, verify=False)

        if response and response.status_code == 200:
            requestInfo.status = response.status_code

            # 数据清洗 获取页数
            soup = BeautifulSoup(response.content.decode('gbk'), 'html5lib')
            soupitems = soup.find_all('div', class_='rt')
            # 第0个是总职位数  第1个是页数标签
            pageNumber = soupitems[1].getText()
            pageNumber = pageNumber.split('/')[1]
            pageNumber = pageNumber.strip()

            if pageNumber:
                pageNumber = int(pageNumber)

            else:
                pageNumber = 0
            logger.debug('number {}'.format(pageNumber))

            baseUrl = url.replace('1.html','{}.html')
            logger.debug('base url {}'.format(baseUrl))
            for i in range(1, pageNumber + 1):
                url = baseUrl.format(i)
                logger.debug(url)
                resultInfo = request_variable_init(url)
                resultInfo.requestName = 'job51_http_get_job_list'
                yield resultInfo, None
        else:
            logger.error('request error http code:{}'.format(response.status_code))
            requestInfo.status = response.status_code if response else 0
    except Exception as e:
        logger.exception(sys.exc_info())
        requestInfo.status = 0

    yield requestInfo,None

#获取职位列表
def job51_http_get_job_list( url ):
    try:
        # headers['Referer'] = url
        requestInfo = request_variable_init(url)
        requestInfo.requestName = 'job51_http_get_job_list'

        response = requests.get(url, headers=headers, verify=False)
        if response and response.status_code == 200:
            requestInfo.status = response.status_code

            soup = BeautifulSoup(response.content.decode('gbk'), 'html5lib')
            tableitem = soup.find('div', class_='dw_table')
            soupitems = tableitem.find_all('div', class_='el')
            for i, item in enumerate(soupitems[1:]):
                t1 = item.find('p', class_='t1')
                t2 = item.find('span', class_='t2')
                t3 = item.find('span', class_='t3')
                t4 = item.find('span', class_='t4')
                t5 = item.find('span', class_='t5')
                # 获取  职位名 公司名  工作地点 薪资 发布时间 (职位URL) (公司URL)
                itemvalue = [t1.a.getText().strip(), t2.a.getText(), t3.getText(), t4.getText(), t5.getText(),
                             t1.a['href'], t2.a['href']]
                logger.debug(itemvalue)
                # 获取 职位详细信息
                # 职位条件概要 福利概要 职位信息 联系方式 部门信息 公司介绍 公司信息分类
                url = itemvalue[5]
                logger.debug(url)
                resultInfo = request_variable_init(url)
                resultInfo.requestName = 'job51_http_get_job_info'
                yield resultInfo, None
        else:
            logger.error('request error http code:{}'.format(response.status_code))
            requestInfo.status = response.status_code if response else 0
    except Exception as e:
        logger.exception(sys.exc_info())
        requestInfo.status = 0

    yield requestInfo, None

#获取职位详细信息
def job51_http_get_job_info(url):
    try:
        # headers['Referer'] = url
        requestInfo = request_variable_init(url)
        requestInfo.requestName = 'job51_http_get_job_info'

        response = requests.get(url, headers=headers, verify=False)
        if response and response.status_code == 200:
            requestInfo.status = response.status_code

            s_time = time.time()
            # 判断页面是否已入库
            jobInfo = JobInfo()
            jobInfo.url = url
            md5 = hashlib.md5()
            md5.update(url.encode('utf-8'))
            jobInfo.jobId = md5.hexdigest()
            # info.jobId = hash(url)
            logger.debug('job info {} {}'.format(jobInfo.jobId, url))
            jobInfo.sourceId = '51job'
            jobInfo.sourceDate = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

            info = dbsession.query(JobInfo).filter_by(jobId=jobInfo.jobId).first()
            if info:
                logger.warning('table query exists %s' % (jobInfo.jobId))
                return requestInfo, None

            if urllib.parse.urlparse(url).netloc == 'carrefour.51job.com':
                logger.warning('%s cant parse' % (url))
                e_time = time.time()
                logger.debug(e_time - s_time)
                jobInfo.parseTime = e_time - s_time
                return requestInfo, None

            soup = BeautifulSoup(response.content.decode('gbk'), 'html5lib')
            # 遇到print soup.prettify()终端字符集问题 设置pycharm Editor->File Encodings 字符集utf8解决
            # print(soup.prettify())

            # print(soup.prettify())
            # with open('D:\project\python\study\myhttp\html.txt', 'w', encoding='utf8') as fd:
            #     fd.write(response.content.decode('gbk'))

            # 企业名
            tag = soup.find('a', class_='catn')
            if tag:
                jobInfo.companyName = tag.get_text().strip()

            # 企业类型  规模 经营范围
            companyTags = soup.find('div', class_='com_tag').find_all('p')
            if companyTags:
                for tag in companyTags:
                    if 'i_flag' in str(tag):
                        # print(tag.get_text().strip())
                        jobInfo.companyType = tag.get_text().strip()
                    elif 'i_people' in str(tag):
                        # print(tag.get_text().strip())
                        jobInfo.companyScale = tag.get_text().strip()
                    elif 'i_trade' in str(tag):
                        trades = tag.find_all('a')
                        tradeList = []
                        for trade in trades:
                            # print(trade.get_text().strip())
                            tradeList.append(trade.get_text().strip())
                        jobInfo.companyTrade = ','.join(tradeList)

            # 职位名
            tag = soup.find('h1')
            if tag:
                jobInfo.jobName = tag.get_text().strip()

            # 职位薪水
            tag = soup.find('div', class_='cn').find('strong')
            if tag:
                jobInfo.jobPay = tag.get_text().strip()

            # 职位条件概要
            tag = soup.find('div', class_='cn').find('p', class_='msg ltype')
            edus = ['初中', '中专', '中技', '大专', '高中', '本科', '硕士', '博士']
            if tag:
                jobTypeListTmp = tag.get_text().split('|')
                jobTypes = [item.strip() for item in jobTypeListTmp]
                for item in jobTypes:
                    if '经验' in item:
                        jobInfo.jobYear = item
                    elif '人' in item:
                        jobInfo.jobMember = item
                    elif '发布' in item:
                        jobInfo.jobDate = item
                    elif item in edus:
                        jobInfo.jobEdu = item
                    else:
                        pass
                        # print(item)

            # 福利待遇
            welfareTags = soup.find('div', class_='cn').find('div', class_='t1').find_all('span')
            welfareList = []
            if welfareTags:
                for item in welfareTags:
                    # print(item.get_text().strip())
                    welfareList.append(item.get_text().strip())
            jobInfo.companyWelfare = ','.join(welfareList)

            bordeTags = soup.find('div', class_='tCompany_main').find_all('div', class_='tBorderTop_box')
            for i, item in enumerate(bordeTags):
                # print(i,item.h2.get_text())
                if item.h2.get_text() == '职位信息':
                    pass
                elif item.h2.get_text() == '联系方式':
                    try:
                        tag = item.find('div', class_='bmsg inbox').find('p', class_='fp')
                        if tag:
                            jobInfo.jobAddr = tag.get_text().strip()
                            # print(jobInfo.jobAddr)
                    except AttributeError as e:
                        print('联系方式 查找失败')
                elif item.h2.get_text() == '部门信息':
                    # 部门信息
                    # companyBm = soup.find_all('div', class_='tBorderTop_box')[2].find('div', class_='bmsg inbox').get_text().strip()
                    # print(companyBm)
                    pass
                elif item.h2.get_text() == '公司信息':
                    pass

            # 公司信息
            jobDescribe = []
            jobDescribeTags = soup.find('div', class_='bmsg job_msg inbox').find_all('p')
            if jobDescribeTags:
                for tag in jobDescribeTags:
                    jobDescribe.append(tag.get_text().strip())
            jobInfo.jobDesc = ''.join(jobDescribe)

            e_time = time.time()
            jobInfo.parseTime = e_time - s_time

            return requestInfo, jobInfo
        else:
            logger.error('request error http code:{}'.format(response.status_code))
            requestInfo.status = response.status_code if response else 0
    except Exception as e:
        logger.exception(sys.exc_info())
        requestInfo.status = 0

    return requestInfo, None

def request_workflow_thread():
    while True:
        try:
            priority,requestInfo,param = requestQueue.get(block=True, timeout=10)
            requestQueue.task_done()
            logger.error('PriorityQueue size {}'.format(requestQueue.qsize()))
            logger.debug('requestQueue func {} url {} urlid {}'.format( requestInfo.requestName, requestInfo.requestUrl, requestInfo.urlId ))
        except Exception as e:
            logger.exception(sys.exc_info())
            logger.error('request_workflow_thread queue empty')
            break

        if requestInfo and requestInfo.requestName:
            logger.debug('run {} params {}'.format(requestInfo.requestName,requestInfo.requestUrl))
            results=eval(requestInfo.requestName)(requestInfo.requestUrl)

            # 判断函数是否是生成器
            if isgeneratorfunction(eval(requestInfo.requestName)):
                logger.debug('isgeneratorfunction {} true'.format(requestInfo.requestName))

                for resultInfo,result in results:
                    if resultInfo.status == 999:
                        logger.debug('PriorityQueue put {},{} '.format(resultInfo.requestName,resultInfo.requestUrl))
                        requestQueue.put( (PRIORITYDEFINE[requestInfo.requestName], resultInfo, result) )
                    else:
                        if isinstance(result,list):
                            for item in result:
                                if isinstance(item, JobInfo):
                                    dbsession.add(item)
                        elif isinstance(result, JobInfo):
                            dbsession.add(result)
                    request_info_update_insert(resultInfo)
                    # info = dbsession.query(RequestInfo).filter(RequestInfo.urlId == resultInfo.urlId).first()
                    # if info:
                    #     info.status = resultInfo.status
                    #     info.updateTime = datetime.datetime.now().time()
                    # else:
                    #     dbsession.add(resultInfo)

                    try:
                        dbsession.commit()
                    except Exception as e:
                        logger.exception(sys.exc_info())
                        logger.error('dbsession error')
                        dbsession.rollback()
            else:
                logger.debug('isgeneratorfunction {} false'.format(requestInfo.requestName))
                resultInfo, result = results

                if isinstance(result, list):
                    for item in result:
                        if isinstance(item, JobInfo):
                            dbsession.add(item)
                elif isinstance(result, JobInfo):
                    dbsession.add(result)

                request_info_update_insert(resultInfo)
                # info = dbsession.query(RequestInfo).filter(RequestInfo.urlId == resultInfo.urlId).first()
                # if info:
                #     info.status = resultInfo.status
                #     info.updateTime = datetime.datetime.now().time()
                # else:
                #     dbsession.add(resultInfo)

                if resultInfo.status == 999:
                    logger.debug('PriorityQueue put {},{} '.format(resultInfo.requestName, resultInfo.requestUrl))
                    requestQueue.put( (PRIORITYDEFINE[requestInfo.requestName], resultInfo, result) )

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
    max_workers = 2
    threadPool = ThreadPoolExecutor(max_workers=max_workers)
    for i in range(max_workers):
        obj=threadPool.submit(request_workflow_thread)
        threadObjs.append(obj)

    requestQueue.join()
    for _ in as_completed(threadObjs):
        logger.debug('one thread over')

    logger.debug('main threads over')

def init_scrapy_work():
    result = dbsession.query(RequestInfo).first()
    if result is None:
        url = 'https://js.51jobcdn.com/in/resource/js/2020/search/common.6ce831ef.js'
        requestInfo = request_variable_init(url)
        requestInfo.requestName = 'job51_http_get_city_code'
        requestQueue.put((PRIORITYDEFINE[requestInfo.requestName], requestInfo, None))
    else:
        logger.debug('scrapy reboot from db')
        infos = dbsession.query(RequestInfo).filter_by( status = '999').all()
        for item in infos:
            logger.debug('scrapy reboot from db {}'.format(item))
            requestQueue.put((PRIORITYDEFINE[item.requestName], item, None))

    print(requestQueue.qsize())

def test():
    # url = 'https://js.51jobcdn.com/in/resource/js/2020/search/common.6ce831ef.js'
    # results = job51_http_get_city_code(url)
    # for item in results:
    #     print(item)

    # url = 'https://search.51job.com/list/010000,000000,0000,00,9,99,%2520,2,1.html'
    # results = job51_http_get_page_total(url)
    # for item in results:
    #     print(item)

    # url = 'https://search.51job.com/list/010000,000000,0000,00,9,99,%2520,2,2000.html'
    # results = job51_http_get_job_list( url )
    # for item in results:
    #     print(item)

    url = 'http://cofco.51job.com/sc/show_job_detail.php?jobid=120045626'
    results = job51_http_get_job_info( url )
    print(results)

    # url = 'https://js.51jobcdn.com/in/resource/js/2020/search/common.6ce831ef.js'
    # requestInfo = request_variable_init(url)
    # requestInfo.requestName = 'job51_http_get_city_code'
    #
    # cnt = request_info_update_insert(requestInfo)
    # print(cnt)
    # dbsession.commit()

    # result = dbsession.query(RequestInfo).first()
    # print(result)

    # cnt = dbsession.query(RequestInfo).filter_by( status = '999').count()
    # if cnt>0:
    #     print('query')
    #     infos = dbsession.query(RequestInfo).filter_by( status = '999').all()
    #     for item in infos:
    #         requestQueue.put((1, item, None))
    #     print(requestQueue.qsize())
    pass

if __name__=='__main__':
    init_scrapy_work()
    scrapy_work( )
    # test()
