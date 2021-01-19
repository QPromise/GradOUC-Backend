#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: qinchangshuai(cs_qin@qq.com) 
Date: 2021/1/19 10:28 
"""
import datetime
import logging

import requests

from OUC.core.utils.session import session

url = "http://id.ouc.edu.cn:8071/sso/login?service=http%3A%2F%2Fpgs.ouc.edu.cn%2Fallogene%2Fpage%2Fhome.htm%3B"


def keep_alive():
    try:
        session.get(url, timeout=10, allow_redirects=False)
    except requests.RequestException:
        logging.warning('无法连接至教务系统')


scheduler.add_job(keep_alive, 'interval', seconds=10, next_run_time=datetime.datetime.now())
