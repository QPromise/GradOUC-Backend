#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: qinchangshuai(cs_qin@qq.com) 
Date: 2021/1/20 9:49 
"""

import requests
import time
import threading

from OUC import log

logger = log.logger


class ProxyIP(object):
    _instance_lock = threading.Lock()
    api_url = "https://dps.kdlapi.com/api/getdps/?orderid=901105509469578&num=1&area=%E5%B1%B1%E4%B8%9C&pt=1&f_et=1&dedup=1&format=json&sep=1"
    proxy_ip = None
    get_ip_time = None
    rest_time = None
    count = 0

    def __init__(self):
        pass

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(ProxyIP, "_instance"):
            with ProxyIP._instance_lock:
                if not hasattr(ProxyIP, "_instance"):
                    ProxyIP._instance = object.__new__(cls)
        return ProxyIP._instance

    @classmethod
    def update_proxy_ip(cls):
        try:
            # res = {"msg": "", "code": 0, "data": {"count": 1, "proxy_list": ["122.4.52.220:19012,1559"], "order_left_count": 997, "dedup_count": 1}}
            get_result = requests.get(cls.api_url).json()['data']['proxy_list'][0].split(",")
            proxy_ip, rest_time = get_result[0], get_result[1]
            get_ip_time = int(time.time())
            cls.proxy_ip = proxy_ip
            cls.rest_time = int(rest_time)
            cls.get_ip_time = get_ip_time
            cls.count += 1
            logger.warning("%s生成了第%s个IP[%s]，剩余时间%ss" % (get_ip_time, cls.count, proxy_ip, rest_time))
        except Exception as e:
            logger.error("获取ip异常%s" % e)
            cls.proxy_ip = None
            cls.get_ip_time = None
            cls.rest_time = None

    @classmethod
    def checkout_ip(cls):
        if cls.proxy_ip is None:
            cls.update_proxy_ip()
        else:
            cur_time = int(time.time())
            if cur_time - cls.get_ip_time >= (cls.rest_time - 1):
                cls.update_proxy_ip()

    @classmethod
    def get_ip(cls):
        username = "cs_qin"
        password = "7wl4jvhz"
        proxies = {
            "http": "http://%s:%s@%s/" % (username, password, cls.proxy_ip),
            "https": "http://%s:%s@%s/" % (username, password, cls.proxy_ip)
        }
        return proxies