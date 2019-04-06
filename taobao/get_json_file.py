from MyModel.models import Analyse
from django.shortcuts import render
from django.http import HttpResponse
import re
import json


def get_json(taobao_id):

    try:
        analyse = Analyse.objects.get(analyse_id=taobao_id)
        print(analyse.id)
        return analyse.analyse_positive_prob
    except Analyse.DoesNotExist:
        print("查询不存在")
        return None


def get_json_url(request):
    if request.GET:
        taobao_id = request.GET['taobao_id']
        print(taobao_id)

    json = get_json(taobao_id)

    if json:
        return HttpResponse(json)
    else:
        return HttpResponse(taobao_id)

def get_json_url_html(request):
    #test
    context = {}
    context['hello'] = 'Hello World!'
    # if request.GET:
    #     taobao_id = request.GET['taobao_id']
    #     print(taobao_id)

    #准备图表数据
    taobao_id = '569931218730'
    json_str = get_json(taobao_id)

    #转list，排序
    json_str = re.sub(' ', '', json_str[1:-1]).split(",")
    json_str.sort(key=None, reverse=False)

    #转str
    str ="[" + ",".join(json_str).__add__("]")
    print(str)

    context['json'] = str


    #准备图表颜色
    color = ""
    for co in json_str:
        co = round(float(co)*255)
        co_color = "'rgba({0}, {1}, 100, 0.6)',".format(255 - co, co)
        color = color.__add__(co_color)

    context['color'] = color


    return render(request, 'get_more_analyse.html', context)
