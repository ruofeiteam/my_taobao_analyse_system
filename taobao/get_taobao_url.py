# -*- coding: utf-8 -*-

from django.shortcuts import render
import re
from django.views.decorators import csrf
import requests
from MyModel.models import Taobao
from django.http import HttpResponse


def mian_taobao(request):
    return render(request, "post_taobao_url.html")


def search_post(request):  # 接收ajax
    if request.POST:
        taobao_url = request.POST['taobao_url']

        if_taobao_url = r"https://item.taobao.com/item.htm"  # 判断是否为正确url
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
        if if_new_taobao_id:  #数据库中存在相应信息，直接返回
            ctx = Taobao.objects.filter(taobao_id=taobao_id[0]).values('taobao_name')
            return HttpResponse(ctx)
            # update_taobao_info = Taobao.objects.get(taobao_id=taobao_id[0])
            # update_taobao_info.taobao_price_now = taobao_price_now[0]
            # update_taobao_info.taobao_shop_name = taobao_shop_name[0]
            # update_taobao_info.taobao_url = taobao_url
            # update_taobao_info.taobao_name = taobao_name[0]
            # update_taobao_info.save()
        else:             #不存在，加入数据库，加入爬取池
            taobao_add = Taobao()
            taobao_add.taobao_price_now = taobao_price_now[0]
            taobao_add.taobao_shop_name = taobao_shop_name[0]
            taobao_add.taobao_url = taobao_url
            taobao_add.taobao_id = taobao_id[0]
            taobao_add.taobao_name = taobao_name[0]
            taobao_add.save()
            ctx = "Success，等待分析"
            #加入线程池


            return HttpResponse(ctx)

        ctx = "other"
        return HttpResponse(ctx)


    # print(taobao_shop_name[0].encode('ascii').decode('unicode_escape'))  #ascii解码
