from MyModel.models import Analyse
from MyModel.models import Spider
from MyModel.models import Taobao
from django.shortcuts import render
from django.http import HttpResponse
import re
import random


def get_barjson(taobao_id):
    try:
        analyse = Analyse.objects.get(analyse_id=taobao_id)
        return analyse.analyse_positive_prob
    except Analyse.DoesNotExist:
        print("情感倾向查询不存在")
        return None


def get_piejson(taobao_id):
    try:
        spider = Spider.objects.get(spider_id=taobao_id)
        return spider.spider_detail_Common
    except Spider.DoesNotExist:
        print("总体评价查询不存在")
        return None


def get_taobao_name(taobao_id):
    try:
        taobao = Taobao.objects.get(taobao_id=taobao_id)
        return taobao.taobao_name
    except Taobao.DoesNotExist:
        print("宝贝名称查询不存在")
        return None


def get_json_url(request):
    if request.GET:
        taobao_id = request.GET['taobao_id']
        print(taobao_id)

    json = get_barjson(taobao_id)

    if json:
        return HttpResponse(json)
    else:
        return HttpResponse(taobao_id)


def get_iframe_html(request):
    context = {}
    context['hello'] = 'Hello World!'
    if request.GET:
        taobao_id = request.GET['taobao_id']
        print("get_id：" + taobao_id)
        if taobao_id == None:
            taobao_id = '569931218730'

        # 准备宝贝名称
        taobao_name = get_taobao_name(taobao_id)
        print(taobao_name)

        context['taobao_name'] = taobao_name

        # 准备图表数据
        json_bar = get_barjson(taobao_id)
        if json_bar == None:
            return HttpResponse("柱状图ID错误")
        # 转list，排序
        json_bar = re.sub(' ', '', json_bar[1:-1]).split(",")
        json_bar.sort(key=None, reverse=False)
        # 转str
        barstr = ",".join(json_bar)

        if barstr == "":
            context['empty_bar'] = "柱状图没有有效的评论数据"
            print("正向情感数组为空")
        else:
            print("正向情感数组：" + barstr)
        context['barlables'] = context['bardata'] = barstr
        # 准备图表颜色
        barcolor = ""
        ran_num = round(random.uniform(0, 255))
        for co in range(len(json_bar)):
            co = round(float(co) * 255)
            co_color = "'rgba({0}, {1}, {2}, 0.8)',".format(255 - co, co, ran_num)
            barcolor = barcolor.__add__(co_color)
        context['barcolor'] = barcolor

        # 准备饼图数据
        json_pie = get_piejson(taobao_id)
        if json_pie == None:
            return HttpResponse("饼图ID错误")

        pie_title = re.findall(r"\"title\":\"(.+?)\"", json_pie)
        pie_value = re.findall(r"\{\"count\":(.+?),\"", json_pie)
        if len(pie_value) == 0:
            context['empty_pie'] = "饼图没有有效的评价数据"
            print("总体评价数组为空")
        else:
            print("总体评价分类：" + str(pie_title))
            print("总体评价数值：" + str(pie_value))
        context['pielables'] = pie_title
        context['piedata'] = pie_value



        piecolor = ""
        for lo in range(len(json_bar)):
            lo = round(random.uniform(0, 0.1) * 2550)
            lo_color = "'rgba({0}, {1}, {2}, 0.8)',".format(round(255 - lo / 2), lo * 2, lo)
            piecolor = piecolor.__add__(lo_color)
        context['piecolor'] = piecolor

        return render(request, 'get_more_analyse.html', context)
    return HttpResponse("未获取ID")
