# -*- coding: utf-8 -*-

import threading



def start_analyse(taobao_id):
    pass






class myThread(threading.Thread):
    def __init__(self, taobao_id):
        threading.Thread.__init__(self)
        self.taobao_id = taobao_id

    def run(self):
        print("开启分析线程： " + self.name)
        # 获取锁，用于线程同步
        threadLock.acquire()
        start_analyse(self.taobao_id)
        # 释放锁，开启下一个线程
        threadLock.release()


threadLock = threading.Lock()
threads = []


def start_thread(taobao_id):
    # 创建新线程
    thread = myThread(taobao_id)

    # 开启新线程
    thread.start()
    threads.append(thread)