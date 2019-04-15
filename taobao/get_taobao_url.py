# -*- coding: utf-8 -*-

from django.shortcuts import render
import re
from django.views.decorators import csrf
import requests
from MyModel.models import Taobao
from MyModel.models import Mail
from django.http import HttpResponse
from .taobao_spider import start_thread_spider

import configparser, os

# 读config.ini文件
dir_now = os.path.dirname(__file__)
conf = configparser.ConfigParser()
conf.read(dir_now + '/config.ini')


def main_taobao(request):
    context = {}
    context['check_url'] = conf.get('taobao', 'url')
    return render(request, 'post_taobao_url.html', context)
    # return render(request, "post_taobao_url.html")


def more_post(request):  # 接收多条输入
    if request.POST:
        urls = request.POST['taobao_url']
        email = request.POST['email']
        urls = urls.split()
        for url in urls:
            ctx = do_url(url, email)
            return HttpResponse(ctx)
        ctx = "more时未知错误"
        return HttpResponse(ctx)


def do_url(taobao_url, email):  # 分离url处理方法

    # if_taobao_url = r"https://item.taobao.com/item.htm"  # 判断是否为正确url
    if_taobao_url = conf.get('taobao', 'url')  # 判断是否为正确url
    if if_taobao_url != taobao_url[0:len(if_taobao_url)]:
        ctx = "Not a valid URL,当前仅支持淘宝评论分析"
        return ctx

    r = requests.get(taobao_url, allow_redirects=False)
    if_200 = r.status_code  # 判断响应状态码
    if if_200 != 200:
        if if_200 == 302:  # 判断是否302跳转
            r.close()
            ctx = r"您查看的宝贝不存在"
            return ctx
        ctx = "ERROR"
        r.close()
        return ctx

    taobao_detail = r.text
    r.close()
    taobao_shop_name = re.findall(r"shopName         : \'(.+?)\'\,", taobao_detail)
    taobao_name = re.findall(r"\<title\>(.+?)-淘宝网\<\/title\>", taobao_detail)
    taobao_price_now = re.findall(r"\<em class=\"tb-rmb-num\"\>(.+?)\<\/em\>", taobao_detail)
    taobao_id = re.findall(r"itemId           : \'(.+?)\'\,", taobao_detail)

    if_new_taobao_id = Taobao.objects.filter(taobao_id=taobao_id[0])
    if if_new_taobao_id:  # 数据库中存在相应信息，直接返回

        # 取结果
        ctx = taobao_id[0]
        return ctx

        start_thread_spider(taobao_id[0])  # 防止意外存入taobao未存入spider
        ctx = "取结果时未知错误"
        return ctx
    else:  # 不存在，加入数据库，加入爬取池
        taobao_add = Taobao()
        taobao_add.taobao_price_now = taobao_price_now[0]
        taobao_add.taobao_shop_name = taobao_shop_name[0]
        taobao_add.taobao_url = taobao_url
        taobao_add.taobao_id = taobao_id[0]
        taobao_add.taobao_name = taobao_name[0]
        taobao_add.save()

        # 加入线程池
        start_thread_spider(taobao_id[0])
        # 加入邮箱
        email_result = save_email(taobao_id[0], email)
        if email_result:
            ctx = "未找到结果，等待分析，请及时查看邮箱"
        else:
            ctx = "未找到结果，等待分析，请稍后再试，若想及时得到信息，请勾选并输入邮箱"

        return ctx

    ctx = "未知错误，联系管理员"
    return ctx


def search_post(request):  # 接收ajax，高耦合，已抛弃使用
    if request.POST:
        taobao_url = request.POST['taobao_url']
        print("url：" + taobao_url)
        email = request.POST['email']
        print("email：" + email)

        # if_taobao_url = r"https://item.taobao.com/item.htm"  # 判断是否为正确url
        if_taobao_url = conf.get('taobao', 'url')
        if if_taobao_url != taobao_url[0:len(if_taobao_url)]:
            ctx = "Not a valid URL,当前仅支持淘宝评论分析"
            return HttpResponse(ctx)

        r = requests.get(taobao_url, allow_redirects=False)
        if_200 = r.status_code  # 判断响应状态码
        if if_200 != 200:
            if if_200 == 302:  # 判断是否302跳转
                r.close()
                ctx = r"您查看的宝贝不存在"
                return HttpResponse(ctx)
            ctx = "ERROR"
            r.close()
            return HttpResponse(ctx)

        taobao_detail = r.text
        r.close()
        taobao_shop_name = re.findall(r"shopName         : \'(.+?)\'\,", taobao_detail)
        taobao_name = re.findall(r"\<title\>(.+?)-淘宝网\<\/title\>", taobao_detail)
        taobao_price_now = re.findall(r"\<em class=\"tb-rmb-num\"\>(.+?)\<\/em\>", taobao_detail)
        taobao_id = re.findall(r"itemId           : \'(.+?)\'\,", taobao_detail)

        if_new_taobao_id = Taobao.objects.filter(taobao_id=taobao_id[0])
        if if_new_taobao_id:  # 数据库中存在相应信息，直接返回

            # 取结果
            ctx = taobao_id[0]
            return HttpResponse(ctx)

            start_thread_spider(taobao_id[0])  # 防止意外存入taobao未存入spider
            return HttpResponse(ctx)
        else:  # 不存在，加入数据库，加入爬取池
            taobao_add = Taobao()
            taobao_add.taobao_price_now = taobao_price_now[0]
            taobao_add.taobao_shop_name = taobao_shop_name[0]
            taobao_add.taobao_url = taobao_url
            taobao_add.taobao_id = taobao_id[0]
            taobao_add.taobao_name = taobao_name[0]
            taobao_add.save()

            # 加入线程池
            start_thread_spider(taobao_id[0])
            # 加入邮箱
            email_result = save_email(taobao_id[0], email)
            if email_result:
                ctx = "未找到结果，等待分析，请及时查看邮箱"
            else:
                ctx = "未找到结果，等待分析，请稍后再试，若想及时得到信息，请勾选并输入邮箱"

            return HttpResponse(ctx)

        ctx = "未知错误，联系管理员"
        return HttpResponse(ctx)
    ctx = "不支持的方法"
    return HttpResponse(ctx)


# 保存待发送的邮箱
def save_email(taobao_id, email):
    if email == "none":
        return 0
    else:
        if_mail = Mail.objects.filter(taobao_id=taobao_id, mail=email)
        if if_mail:
            return 0
        else:
            mail = Mail()
            mail.taobao_id = taobao_id
            mail.mail = email
            mail.save()
        return 1
