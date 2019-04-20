from django.contrib import admin

# Register your models here.

from MyModel.models import Taobao
from MyModel.models import Spider
from MyModel.models import Analyse
from MyModel.models import Mail


@admin.register(Taobao)
class TaobaoAdmin(admin.ModelAdmin):
    list_display = ('taobao_id', 'taobao_name', 'taobao_price_now', 'taobao_time',)
    list_filter = ('taobao_time',)
    search_fields = ('taobao_name', 'taobao_id',)  # 搜索字段
    date_hierarchy = 'taobao_time'  # 详细时间分层筛选　


@admin.register(Spider)
class SpiderAdmin(admin.ModelAdmin):
    list_display = ('spider_id', 'spider_time',)
    list_filter = ('spider_time',)
    search_fields = ('spider_id',)
    date_hierarchy = 'spider_time'


@admin.register(Analyse)
class AnalyseAdmin(admin.ModelAdmin):
    list_display = ('analyse_id', 'analyse_time',)
    list_filter = ('analyse_time',)
    search_fields = ('analyse_id',)
    date_hierarchy = 'analyse_time'


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('taobao_id', 'mail', 'add_time',)
    list_filter = ('add_time', 'taobao_id', 'mail',)
    search_fields = ('taobao_id', 'mail',)
    date_hierarchy = 'add_time'
