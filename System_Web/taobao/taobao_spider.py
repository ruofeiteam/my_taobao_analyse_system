# -*- coding: utf-8 -*-

import re
import requests
import json

from MyModel.models import Spider
import threading
from .taobao_analyse import start_thread_analyse


def Comment_Spider(taobao_id):  # 获取总体评价
    parmar = {'auctionNumId': taobao_id}
    taobao_detailCommon_url = r"https://rate.taobao.com/detailCommon.htm"
    r = requests.get(taobao_detailCommon_url, params=parmar)

    spider_detail_common = r.text
    r.close()

    return (spider_detail_common)


# rate.taobao.com/feedRateList.htm?auctionNumId=584067666712&currentPageNum=180&pageSize=100 每个评论
def One_Page_Spider(taobao_id, page_num, page_size="1000"):  # 获取单页评价
    parmar = {'auctionNumId': taobao_id, 'currentPageNum': page_num, 'pageSize': page_size}
    cookies = dict(
        x5sec='7b22726174656d616e616765723b32223a223631306230393455676639663036366363623562316139383134753963616132434e61436a755146454a47642b4c65373937717a5767453d227d')
    taobao_one_page_url = r"https://rate.taobao.com/feedRateList.htm"
    r = requests.get(taobao_one_page_url, params=parmar, cookies=cookies)

    spider_one_page_common = r.text
    r.close()

    return (spider_one_page_common)


def All_Spider(taobao_id):  # 获取所有评论
    list_content = []

    for page_num in range(1, 200):
        content = One_Page_Spider(taobao_id, page_num)
        all_content = re.findall(r"\]\,\"content\"\:\"(.+?)\"", content)
        if len(all_content) != 0:
            list_content = list_content + all_content
        else:
            break

    # 加入分析
    start_thread_analyse(list_content, taobao_id)
    #
    return (json.dumps(list_content))
    # return (list_content)


def save_common_mysql(taobao_id):
    print(taobao_id)

    if_new_spider_id = Spider.objects.filter(spider_id=taobao_id)
    if if_new_spider_id:  # 数据库中存在相应信息，直接返回
        print("爬虫数据已存在")
    else:  # 不存在，存入数据库
        detail_comment_json = Comment_Spider(taobao_id)  # 爬取
        all_ages_json = All_Spider(taobao_id)

        if_new_spider_id = Spider.objects.filter(spider_id=taobao_id)
        if if_new_spider_id:  # 数据库中存在相应信息，直接返回
            print("爬虫数据已存在")
        else:  # 不存在，存入数据库
            spider_add = Spider()
            spider_add.spider_id = taobao_id
            spider_add.spider_detail_Common = detail_comment_json
            spider_add.spider_detail_All = all_ages_json
            spider_add.save()
            print("爬虫数据保存完毕")


############################################多线程
class myThread(threading.Thread):
    def __init__(self, taobao_id):
        threading.Thread.__init__(self)
        self.taobao_id = taobao_id

    def run(self):
        print("开启爬虫线程： " + self.name)
        # 获取锁，用于线程同步
        threadLock.acquire()
        save_common_mysql(self.taobao_id)
        # 释放锁，开启下一个线程start_thread
        threadLock.release()


threadLock = threading.Lock()
threads = []


def start_thread_spider(taobao_id):
    # 创建新线程
    thread = myThread(taobao_id)

    # 开启新线程
    thread.start()
    threads.append(thread)
