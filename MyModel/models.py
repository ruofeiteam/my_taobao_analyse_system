# from django.db import models

# Create your models here.

# django-admin startapp Model  #创建APP


# python manage.py migrate   # 创建表结构
# python manage.py makemigrations Model  # 让 Django 知道我们在我们的模型有一些变更
# python manage.py migrate Model   # 创建表结构

# python manage.py makemigrations    #修改model后同步到数据库
# python manage.py migrate


# Create your models here.
from django.db import models


class Taobao(models.Model):  # 创建商品信息
    taobao_name = models.CharField(max_length=100)
    taobao_id = models.CharField(max_length=50)
    taobao_url = models.CharField(max_length=256)
    taobao_shop_name = models.CharField(max_length=100)
    taobao_price_now = models.CharField(max_length=50)
    taobao_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.taobao_name


class Spider(models.Model):  # 创建评论信息
    spider_id = models.CharField(max_length=50)
    spider_detail_Common = models.CharField(max_length=3000)
    spider_detail_All = models.TextField()
    spider_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.spider_id


class Analyse(models.Model):  # 评论分析结果
    analyse_id = models.CharField(max_length=50)
    analyse_positive_prob = models.TextField()
    analyse_negative_prob = models.TextField()
    analyse_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.analyse_id


class Mail(models.Model):  # 邮件-宝贝id
    taobao_id = models.CharField(max_length=50)
    mail = models.CharField(max_length=100)
    add_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.id
