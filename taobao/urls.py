"""taobao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import get_taobao_url
from . import get_json_file

from django.views.generic.base import RedirectView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', get_taobao_url.main_taobao),
    # path('get_taobao_url/', get_taobao_url.search_post),
    path('get_taobao_url/', get_taobao_url.more_post),
    path('get_json/',get_json_file.get_json_url),
    path('analyse/',get_json_file.get_iframe_html),
    path('favicon.ico',RedirectView.as_view(url=r'static/images/favicon.ico')),
]


