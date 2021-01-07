#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: qinchangshuai(cs_qin@qq.com) 
Date: 2020/12/21 9:56 
"""

import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from OUC.core import test_score_subscribe, score_subscribe
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
    scheduler = BackgroundScheduler()
    try:
        # 监控任务
        try:
            scheduler.add_job(get_access_token, trigger='interval', coalesce=True,
                              seconds=530, id='get_access_token')
        except Exception as e:
            logger.error("%s" % e)
        try:
            scheduler.add_job(travel_subscribe_student, trigger='interval', coalesce=True,
                              seconds=550, id='travel_subscribe_student')
        except Exception as e:
            logger.error("%s" % e)
        try:
            scheduler.add_job(update_all_subscribe_student, trigger='interval', coalesce=True,
                              seconds=21600, id='update_all_subscribe_student')
        except Exception as e:
            logger.error("%s" % e)
        # 调度器开始
        logger.debug("调度器开始执行....")
        scheduler.start()
    except Exception as e:
        # 报错则调度器停止执行
        logger.error("调度器停止执行！%s" % e)
        scheduler.shutdown()


start_travel_subscribe_student()

