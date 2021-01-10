"""PgOUC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url, include

import sys, socket
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from OUC.core import score_subscribe
from OUC import log
from OUC import models

logger = log.logger


def get_access_token():
    try:
        if models.Config.objects.all()[0].is_open_subscribe in [1, 2]:
            cur_hour = datetime.datetime.now().strftime('%H:%M')
            if cur_hour <= '02:50' or cur_hour >= '06:00':
                score_subscribe.AccessToken.update_access_token()
    except Exception as e:
        logger.warning("缺少是否订阅的数据列，数据库当前还没migrate%s" % e)


def travel_subscribe_student():
    try:
        if models.Config.objects.all()[0].is_open_subscribe in [1, 2]:
            cur_hour = datetime.datetime.now().strftime('%H:%M')
            if cur_hour <= '02:50' or cur_hour >= '06:00':
                score_subscribe.SubscribeScore.travel_subscribe_student()
    except Exception as e:
        logger.warning("缺少是否订阅的数据列，数据库当前还没migrate%s" % e)


def update_all_subscribe_student():
    try:
        if models.Config.objects.all()[0].is_open_subscribe in [1, 2]:
            # cur_hour = datetime.datetime.now().strftime('%H:%M')
            # if cur_hour <= '02:50' or cur_hour >= '06:00':
            score_subscribe.SubscribeScore.update_all_subscribe_student()
    except Exception as e:
        logger.warning("缺少是否订阅的数据列，数据库当前还没migrate%s" % e)


def start_travel_subscribe_student():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 47200))
        try:
            scheduler = BackgroundScheduler()
            # 监控任务
            scheduler.add_job(get_access_token, trigger='cron', coalesce=True,
                              minute='*/7', id='get_access_token')
            scheduler.add_job(travel_subscribe_student, trigger='cron', coalesce=True,
                              minute='*/8', id='travel_subscribe_student')
            scheduler.add_job(update_all_subscribe_student, trigger='cron', coalesce=True,
                              hour='*/6', id='update_all_subscribe_student')
            # 调度器开始
            logger.debug("调度器开始执行....")
            scheduler.start()
        except Exception as e:
            # 报错则调度器停止执行
            logger.error("调度器停止执行！%s" % e)
            scheduler.shutdown()
    except Exception as e:
        logger.error("[调度器执行了两遍]%s scheduler has already started!" % e)


start_travel_subscribe_student()

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', include('OUC.urls')),
]
