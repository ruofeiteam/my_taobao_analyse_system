# -*- coding: utf-8 -*-

import threading

from MyModel.models import Analyse


def start_analyse(list_content,taobao_id):
    exclude = ["评价方未及时做出评价,系统默认好评!", "此用户没有填写评价。", "系统默认评论"]
    positive_prob = []
    negative_prob = []
    for text in list_content:
        if text in exclude:
            continue
        else:   ##{'positive_prob': 0.463763, 'confidence': 0.275252, 'negative_prob': 0.536237, 'sentiment': 1}
            text_items = sentiment_classify(text)['items'][0]
            text_positive_prob = text_items['positive_prob']
            positive_prob.append(text_positive_prob)
            text_negative_prob = text_items['negative_prob']
            negative_prob.append(text_negative_prob)

    print(positive_prob)
    print(negative_prob)

    if_new_analyse_id = Analyse.objects.filter(analyse_id=taobao_id)

    if if_new_analyse_id:  # 数据库中存在相应信息，直接返回
        print("分析数据已存在")
    else:  # 不存在，存入数据库
        analyse_add = Analyse()
        analyse_add.analyse_id = taobao_id
        analyse_add.analyse_negative_prob = negative_prob
        analyse_add.analyse_positive_prob = positive_prob
        analyse_add.save()
        print("分析数据保存完毕")



import json, urllib


# 百度Al情感倾向分析
def sentiment_classify(text):
    """
    获取文本的感情偏向（消极 or 积极 or 中立）
    参数：
    text:str 本文
    """
    raw = {"text": "内容"}
    raw['text'] = text
    data = json.dumps(raw).encode('utf-8')
    AT = "24.8a7698581e69872e18cff7218673be26.2592000.1556000633.282335-15834712"
    host = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token=" + AT
    request = urllib.request.Request(url=host, data=data)
    request.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    rdata = json.loads(content)
    return rdata


class myThread(threading.Thread):
    def __init__(self, list_content,taobao_id):
        threading.Thread.__init__(self)
        self.list_content = list_content
        self.taobao_id = taobao_id

    def run(self):
        print("开启分析线程： " + self.name)
        # 获取锁，用于线程同步
        threadLock.acquire()
        start_analyse(self.list_content,self.taobao_id)
        # 释放锁，开启下一个线程
        threadLock.release()


threadLock = threading.Lock()
threads = []


def start_thread_analyse(list_content,taobao_id):
    # 创建新线程
    thread = myThread(list_content,taobao_id)

    # 开启新线程
    thread.start()
    threads.append(thread)
