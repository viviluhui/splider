# -*- coding:utf-8 -*-
import sys
import time
from concurrent.futures import ThreadPoolExecutor,as_completed
from inspect import isgeneratorfunction
from weibo_utils import logger,requestQueue,sessionQueue,request_variable_init,PRIORITYDEFINE
from weibo_login import weibo_login_cookie
from weibo_parser import weibo_http_get_navigation_page_list,weibo_http_get_navigation_page_url,weibo_http_get_navigation
from weibo_models import dbsession,WeiboUser,RequestInfo,request_info_update_insert

def request_workflow_thread():
    while True:
        try:
            session = sessionQueue.get(block=True, timeout=10)
            sessionQueue.task_done()
            sessionQueue.put(session)

            priority,requestInfo,param = requestQueue.get(block=True, timeout=10)
            requestQueue.task_done()
            logger.debug('PriorityQueue size {}'.format(requestQueue.qsize()))
        except Exception as e:
            logger.exception(sys.exc_info())
            logger.error('request_workflow_thread queue empty')
            break

        time.sleep(20)
        if requestInfo and requestInfo.requestName:
            logger.debug('run {} params {}'.format(requestInfo.requestName,requestInfo.requestUrl))
            results=eval(requestInfo.requestName)(requestInfo.requestUrl, session)

            # 判断函数是否是生成器
            if isgeneratorfunction(eval(requestInfo.requestName)):
                logger.debug('isgeneratorfunction {} true'.format(requestInfo.requestName))
                for resultInfo,result in results:
                    if resultInfo.status == 999:
                        logger.debug('PriorityQueue put {},{} '.format(resultInfo.requestName,resultInfo.requestUrl))
                        requestQueue.put((PRIORITYDEFINE[resultInfo.requestName], resultInfo, result))
                    else:
                        if isinstance(result,list):
                            for item in result:
                                if isinstance(item, WeiboUser):
                                    dbsession.add(item)
                        elif isinstance(result, WeiboUser):
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

                if isinstance(result, list):
                    for item in result:
                        if isinstance(item, WeiboUser):
                            dbsession.add(item)
                elif isinstance(result, WeiboUser):
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
    max_workers = 1
    threadPool = ThreadPoolExecutor(max_workers=max_workers)
    for i in range(max_workers):
        obj=threadPool.submit(request_workflow_thread)
        threadObjs.append(obj)

    requestQueue.join()
    for _ in as_completed(threadObjs):
        logger.debug('one thread over')

    logger.debug('main threads over')

def init_session_pool():
    user='18162758696'
    password='qgjiqpl1987'
    session = weibo_login_cookie(user, password)
    sessionQueue.put(session)

def init_scrapy_work():
    init_session_pool()

    result = dbsession.query(RequestInfo).first()
    if result is None:
        url = 'https://d.weibo.com/1087030002_2986_top'
        requestInfo = request_variable_init(url)
        requestInfo.requestName = 'weibo_http_get_navigation_page_list'
        requestQueue.put((PRIORITYDEFINE[requestInfo.requestName], requestInfo, None))
    else:
        logger.debug('scrapy reboot from db')
        infos = dbsession.query(RequestInfo).filter_by( status = '999').all()
        for item in infos:
            logger.debug('scrapy reboot from db {}'.format(item))
            requestQueue.put((1, item, None))

def test():
    user='18162758696'
    password='qgjiqpl1987'
    session = weibo_login_cookie(user, password)

    # url = 'https://d.weibo.com/1087030002_2986_top'
    # results = weibo_http_get_navigation_page_list(url, session=session)
    # for k,v in results:
    #     pass
    #
    # url = 'https://d.weibo.com/1087030002_2976_1004_1'
    # url = 'https://d.weibo.com/1087030002_2975_1003_0'
    # url = 'https://d.weibo.com/1087030002_2976_1003_9'
    # results = weibo_http_get_navigation_page_url(url,session)
    # for k,v in results:
    #     pass

    url = 'https://d.weibo.com/1087030002_2976_1003_9?pids=Pl_Core_F4RightUserList__4&page=5#Pl_Core_F4RightUserList__4'
    results = weibo_http_get_navigation(url, session)
    print(results)

if __name__ == '__main__':
    init_scrapy_work()
    scrapy_work()
    # test()

