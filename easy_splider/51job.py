# -*- coding: utf-8 -*-
import requests
import random
import json
import os
from bs4 import BeautifulSoup
from models import *
import hashlib
import time
import urllib.parse
import math
import re

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
]
headers = {
           'User-Agent': random.choice(USER_AGENTS),
           'Accept - Encoding': 'gzip, deflate',
           'Accept - Language': 'zh - CN, zh;q = 0.9',
           'Connection': 'keep-alive'
           }


#获取城市的城市编号
def get_city_code(filename=None):
    '''
    json    load loads
            dump dumps
    :param filename:
    :return:
    '''
    if filename and os.path.exists(filename) and os.path.getsize(filename)>0:
        cityDict = {}
        try:
            with open(filename, 'r', encoding='utf-8') as fp:
                cityDict = json.load(fp)
        except Exception as e:
            print('load json file error')
        else:
            print('load json file ok')
            return cityDict

    url = 'https://js.51jobcdn.com/in/resource/js/2020/search/common.6ce831ef.js'
    headers['Referer'] = url

    reponse = requests.get(url, headers=headers)
    text = reponse.text

    i=text.index('window.area')
    j = text.index('}',i)

    area = text[i:j]
    area = area.replace('window.area={','')

    areaList = area.split(',')
    cityDict = { }

    for item in areaList:
        city=item.split(':')
        cityDict[city[1].strip('\"\t\n')] = city[0].strip('\"\t\n')
    # print(cityDict)

    if filename:
        with open(filename, 'w', encoding='utf-8') as fp:
            # indent，为字符串转行 + 缩进  ensure_ascii为False时内容输出显示正常的中文，而不是转码
            json.dump(cityDict, fp, indent=4, ensure_ascii=False)
    return cityDict

def get_page_total(cityCode, keyword):
    '''
    #获取职位总页数
    :param city_code: 地市编号
    :param keyword: 职位关键字
    :return:
    '''
    url = 'https://search.51job.com/list/' + str(cityCode) +',000000,0000,00,9,99,'+ str(keyword) +',2,1.html'
    print('get page number url: %s' % (url))
    headers['Referer'] = url
    response = requests.get(url, headers)

    #数据清洗 获取页数
    soup = BeautifulSoup(response.content.decode('gbk'), 'html5lib')
    soupitems = soup.find_all('div', class_='rt')
    #第0个是总职位数  第1个是页数标签
    pageNumber = soupitems[1].getText()
    pageNumber = pageNumber.split('/')[1]
    pageNumber = pageNumber.strip()

    if pageNumber:
        pageNumber = int(pageNumber)
        return pageNumber
        # math.ceil(int(pageNumber))
    else:
        return 0

#获取职位列表
def get_page(cityCode, keyword, pageNumber):
    url = 'https://search.51job.com/list/' + str(cityCode) + ',000000,0000,00,9,99,' + str(keyword) + ',2,'+ str(pageNumber) +'.html'
    print('get page url: %s' % (url))
    headers['Referer'] = url
    response = requests.get(url, headers)
    soup = BeautifulSoup(response.content.decode('gbk'), 'html5lib')

    # with open('D:\project\python\study\myhttp\html.txt', 'w') as fd:
    #     fd.write(response.content.decode('gbk'))

    # soupitems = soup.find_all('div', class_=re.compile('el'))

    # def has_six_characters(css_class):
    #     return css_class is not None and css_class == 'el' and len(css_class) == 2
    # soupitems = soup.find_all('div', class_=has_six_characters)

    # soupitems = soup.find_all('div', attrs={'class':'el'})
    # tableitem = soup.find_all('div', id='resultList')

    tableitem = soup.find('div', class_='dw_table')
    soupitems = tableitem.find_all('div', class_='el')
    for i,item in enumerate(soupitems[1:]):
        t1 = item.find('p',class_='t1')
        t2 = item.find('span', class_='t2')
        t3 = item.find('span', class_='t3')
        t4 = item.find('span', class_='t4')
        t5 = item.find('span', class_='t5')
        # 获取  职位名 公司名  工作地点 薪资 发布时间 (职位URL) (公司URL)
        itemvalue = [t1.a.getText().strip(), t2.a.getText(), t3.getText(), t4.getText(), t5.getText(), t1.a['href'],t2.a['href']]
        print(itemvalue)
        #获取 职位详细信息
        #职位条件概要 福利概要 职位信息 联系方式 部门信息 公司介绍 公司信息分类
        s_time = time.time()
        try:
            if get_info(itemvalue[5]) is None:
                continue
        except Exception as e:
            print(e)
            print('url exception: %s '% (itemvalue[5]) )
        e_time = time.time()
        print("use {:.5}s".format(e_time - s_time))
        # time.sleep(1)

#获取职位详细信息
def get_info(url):
    headers['Referer'] = url
    s_time = time.time()
    #判断页面是否已入库
    jobInfo = JobInfo()
    jobInfo.url = url
    md5 = hashlib.md5()
    md5.update(url.encode('utf-8'))
    jobInfo.jobId = md5.hexdigest()
    # info.jobId = hash(url)
    print(jobInfo.jobId,  url)
    jobInfo.sourceId = '51job'
    jobInfo.sourceDate = time.strftime('%Y%m%d', time.localtime(time.time()))

    info = dbsession.query(JobInfo).filter_by(jobId=jobInfo.jobId).first()
    if info:
        print('table query exists %s' % (jobInfo.jobId))
        return None

    if urllib.parse.urlparse(url).netloc == 'carrefour.51job.com':
        print('%s cant parse' % (url) )
        e_time = time.time()
        print(e_time-s_time)
        jobInfo.parseTime = e_time-s_time
        dbsession.add(jobInfo)
        try:
            dbsession.commit()
        except Exception as e:
            dbsession.rollback()
        return None

    response = None
    try:
        response = requests.get(url, headers)
    except Exception as e:
        raise e
    # print(response.encoding)  # 查看网页返回的字符集类型
    # print(response.apparent_encoding)  # 自动判断字符集类型
    # # print(response.content.decode('gb18030'))
    # response.encoding = "gbk"
    # print(response.text)
    if response.status_code != 200:
        return response.status_code

    soup = BeautifulSoup(response.content.decode('gbk'), 'html5lib')
    #遇到print soup.prettify()终端字符集问题 设置pycharm Editor->File Encodings 字符集utf8解决
    # print(soup.prettify())

    # print(soup.prettify())
    # with open('D:\project\python\study\myhttp\html.txt', 'w', encoding='utf8') as fd:
    #     fd.write(response.content.decode('gbk'))

    #企业名

    tag = soup.find('a',class_='catn')
    if tag:
        jobInfo.companyName = tag.get_text().strip()

    #企业类型  规模 经营范围
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

    #职位名
    tag = soup.find('h1')
    if tag:
        jobInfo.jobName = tag.get_text().strip()

    #职位薪水
    tag = soup.find('div', class_='cn').find('strong')
    if tag:
        jobInfo.jobPay =  tag.get_text().strip()

    # 职位条件概要
    tag = soup.find('div', class_='cn').find('p', class_='msg ltype')
    edus = ['初中','中专','中技', '大专', '高中', '本科', '硕士', '博士']
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

    #福利待遇
    welfareTags = soup.find('div', class_='cn').find('div', class_='t1').find_all('span')
    welfareList = []
    if welfareTags:
        for item in welfareTags:
            # print(item.get_text().strip())
            welfareList.append(item.get_text().strip())
    jobInfo.companyWelfare = ','.join(welfareList)

    bordeTags = soup.find('div',class_='tCompany_main').find_all('div', class_='tBorderTop_box')
    for i,item in enumerate(bordeTags):
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
    jobDescribe=[]
    jobDescribeTags = soup.find('div', class_='bmsg job_msg inbox').find_all('p')
    if jobDescribeTags:
        for tag in jobDescribeTags:
            jobDescribe.append(tag.get_text().strip())
    jobInfo.jobDesc = ''.join(jobDescribe)
    # print(jobInfo.jobDesc)

    e_time = time.time()
    print(e_time - s_time)
    jobInfo.parseTime = e_time - s_time
    dbsession.add(jobInfo)
    try:
        dbsession.commit()
    except Exception as e:
        dbsession.rollback()

    return 0

def main():
    cityDict = get_city_code('D:\project\python\study\myhttp\cityjson.txt')

    # 查询条件
    cityName = '武汉'
    cityCode = cityDict.get(cityName)
    print(cityName, cityCode)
    keyword = 'python'
    # 不设职位搜索条件
    keyword = '%2520'

    totalPages = get_page_total(cityCode, keyword)
    print('pages: %d' % (totalPages))

    for i in range(1, totalPages + 1):
        get_page(cityCode, keyword, i)

if __name__=='__main__':

    main()
    # get_info('https://jobs.51job.com/wuhan/121079625.html?s=01&t=0')
    # get_info('https://jobs.51job.com/wuhan-jxq/115980058.html?s=01&t=6')
    # get_info('http://carrefour.51job.com/jobdetail.html?jobid=107908311')
    # get_info('https://jobs.51job.com/wuhan-jxq/115980058.html?s=01&t=0 ')
    # print(urllib.parse.urlparse('http://carrefour.51job.com/jobdetail.html?jobid=107908311'))

    # s_time = time.time()
    # get_info('http://carrefour.51job.com/jobdetail.html?jobid=107908311')
    # e_time = time.time()
    # print("use {:.5}s".format(e_time - s_time))