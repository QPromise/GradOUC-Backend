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
import time
from apscheduler.schedulers.background import BackgroundScheduler

from OUC.core import score_subscribe, score_rank, get_info
from OUC import log
from OUC import models
from OUC.core.package import proxy

logger = log.logger


def student_info_travel():
    try:
        cur_hour = datetime.datetime.now().strftime('%H:%M')
        # if cur_hour >= '22:15' or cur_hour <= '06:00':
        get_info.SpiderInfo.travel_info()
    except Exception as e:
        logger.warning("缺少是否订阅的数据列，数据库当前还没migrate%s" % e)


def score_rank_travel():
    try:
        if models.Config.objects.all()[0].is_open_score_rank_travel in [1, 2]:
            cur_hour = datetime.datetime.now().strftime('%H:%M')
            # if cur_hour >= '23:45' or cur_hour <= '06:00':
            score_rank.ScoreRank.execute_update_students_rank()
    except Exception as e:
        logger.warning("缺少是否订阅的数据列，数据库当前还没migrate%s" % e)


def get_access_token():
    try:
        if models.Config.objects.all()[0].is_open_subscribe in [1, 2]:
            cur_hour = datetime.datetime.now().strftime('%H:%M')
            if cur_hour <= '00:50' or cur_hour >= '06:00':
                score_subscribe.AccessToken.update_access_token()
    except Exception as e:
        logger.warning("缺少是否订阅的数据列，数据库当前还没migrate%s" % e)


def travel_subscribe_students():
    try:
        if models.Config.objects.all()[0].is_open_subscribe in [1, 2]:
            cur_hour = datetime.datetime.now().strftime('%H:%M')
            if cur_hour <= '00:50' or cur_hour >= '06:00':
                score_subscribe.SubscribeScore.travel_subscribe_students()
    except Exception as e:
        logger.warning("缺少是否订阅的数据列，数据库当前还没migrate%s" % e)


def update_all_subscribe_students():
    try:
        if models.Config.objects.all()[0].is_open_subscribe in [1, 2]:
            # cur_hour = datetime.datetime.now().strftime('%H:%M')
            # if cur_hour <= '02:50' or cur_hour >= '06:00':
            score_subscribe.SubscribeScore.update_all_subscribe_student()
    except Exception as e:
        logger.warning("缺少是否订阅的数据列，数据库当前还没migrate%s" % e)


# 删除所有订阅学生
def del_all_subscribe_students():
    score_subscribe.SubscribeScore.del_all_subscribe_students()


def update_info_and_science_college_name():
    rank_students = models.StudentRank.objects.all()
    students = models.Student.objects.all()
    info_students = models.StudentInfo.objects.all()
    travel_begin = time.time()
    for rank_student in rank_students:
        if rank_student.department == "信息科学与工程学院":
            rank_student.department = "信息科学与工程学部"
            rank_student.save()
    for student in students:
        if student.department == "信息科学与工程学院":
            student.department = "信息科学与工程学部"
            student.save()
    for student in info_students:
        if student.department == "信息科学与工程学院":
            student.department = "信息科学与工程学部"
            student.save()
    travel_end = time.time()
    logger.info("更新信息科学与工程学院为学部[%s个]共耗时%s" % (len(rank_students) + len(students) + len(info_students), travel_end - travel_begin))


def start_schedule():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 47200))
        try:
            scheduler = BackgroundScheduler()
            # 监控任务
            scheduler.add_job(get_access_token, trigger='cron', coalesce=True,
                              minute='*/45', id='get_access_token')
            scheduler.add_job(travel_subscribe_students, trigger='cron', coalesce=True,
                              minute='*/40', id='travel_subscribe_students')
            # scheduler.add_job(update_all_subscribe_students, trigger='cron', coalesce=True,
            #                   hour='*/5', id='update_all_subscribe_students')
            # scheduler.add_job(ip_keep_alive, trigger='cron', coalesce=True,
            #                   second='*/1', id='ip_keep_alive')
            # scheduler.add_job(score_rank_travel, trigger='cron', coalesce=True,
            #                   hour='14', minute='50', id='score_rank_travel')
            scheduler.add_job(score_rank_travel, trigger='cron', coalesce=True,
                              hour='13', minute='15', id='score_rank_travel')
            scheduler.add_job(student_info_travel, trigger='cron', coalesce=True,
                              hour='20', minute='30', id='student_info_travel')
            # 调度器开始
            logger.debug("调度器开始执行....")
            scheduler.start()
        except Exception as e:
            # 报错则调度器停止执行
            logger.error("调度器停止执行！%s" % e)
            scheduler.shutdown()
    except Exception as e:
        logger.error("[调度器执行了两遍]%s scheduler has already started!" % e)


start_schedule()
# update_info_and_science_college_name()
# del_all_subscribe_students()

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', include('OUC.urls')),
]
