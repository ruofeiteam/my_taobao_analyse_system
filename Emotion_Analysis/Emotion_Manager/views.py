# -*- encoding: utf-8 -*-
import re
import jieba
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import Emotion_Manager.CEA_LIB.chinese_emotion_analysis as CEA
from Emotion_Manager.Modules.main import getScoreFromString
from snownlp import SnowNLP
from Emotion_Manager.BaiduAl.baiduAl import sentiment_classify as baiduAl
# Create your views here.


# def redirect_to_index(request):
#     return HttpResponseRedirect('/index')
#
#
# def index(request):
#     return render(request, 'Emotion_Manager/index.html', {})


def calculate_accuracy(request):
    # CEA.compare_test()
    print(request.GET['query'])
    print(request.GET['type'])
    text = request.GET['query']
    type = request.GET['type']

    if type == 'MyNLP':
        text = ''.join(text.split())
        text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）～-]+", "", text)
        pos_list = jieba.cut(text, cut_all=False)
        res = CEA.application(CEA.transfer_text_to_moto(list(pos_list)))
        print("基于机器学习：" + str(res))

        return HttpResponse(res)
    elif type == 'DIC':
        print(request.GET['dic'])
        dicType = request.GET['dic']
        score = getScoreFromString(text, int(dicType))
        print("基于字典：" + str(score))
        return HttpResponse(score)
    elif type == 'SnowNLP':
        return HttpResponse(SnowNLP(text).sentiments)
    elif type == "BaiduAl": #未测试
        return HttpResponse(baiduAl(text))



def dict_result(request):
    pass
