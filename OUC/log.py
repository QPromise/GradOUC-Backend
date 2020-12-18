#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
日志类实现

Author: qinchangshuai(qinchangshuai@baidu.com)
Date: 2020/6/7 11:14
"""

import logging
import logging.handlers
import os


class InitLog(object):
    """日志功能初始化"""
    def __init__(self):
        pass

    @staticmethod
    def init_log(log_path, log_name="OUC", level=logging.INFO, when="D", backup=7,
                 format="%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s",
                 datefmt="%Y-%m-%d %H:%M:%S"):
        """
        初始化日志文件

        Args:
            log_path:日志保存路径
            log_name:日志名称
            level:日志信息写入级别，小于该级别信息不写入，DEBUG < INFO < WARNING < ERROR < CRITICAL
            when:拆分日志文件的时间间隔， 'S' : Seconds，'M' : Minutes，'H' : Hours，'D' : Days，'W' : Week day
                默认值为'D'
            backup:保留备份文件的个数，默认值为7
            format:日志信息展示格式，如：ERROR: 2020-06-07 12:32:54,462: mini_spider.py:23 * 12108 nklnlj
            datefmt: 设置日期展示格式

        Raises:
            OSError: 创建日志文件夹失败
        """
        formatter = logging.Formatter(format, datefmt)
        logger = logging.getLogger()
        logger.setLevel(level)

        log_path = log_path if log_path[-1] == '/' else log_path + '/'
        if not os.path.exists(log_path):
            try:
                os.makedirs(log_path)
            except OSError as e:
                logger.error("创建文件夹失败: %s" % e)

        # 该文件记录所有日志
        handler = logging.handlers.TimedRotatingFileHandler(log_path + log_name + ".log",
                                                            when=when,
                                                            backupCount=backup,
                                                            encoding="utf-8")
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # 该文件专门记录warning/error/critical日志
        handler = logging.handlers.TimedRotatingFileHandler(log_path + log_name + ".log.wf",
                                                            when=when,
                                                            backupCount=backup,
                                                            encoding="utf-8")
        handler.setLevel(logging.WARNING)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger


# 初始化日志配置
logger = InitLog.init_log("./log")
