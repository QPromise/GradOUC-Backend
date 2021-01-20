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
    api_url1 = "https://kps.kdlapi.com/api/getkps/?orderid=941111348996336&num=1&pt=1&f_et=1&format=json&sep=1"
    order_url = "https://dev.kdlapi.com/api/getorderexpiretime?orderid=941111348996336&signature=mqk43ei38k3hv455h8evy11hy4rx1s6y"
    api_url = "https://dps.kdlapi.com/api/getdps/?orderid=901105509469578&num=1&area=%E5%B1%B1%E4%B8%9C&pt=1&f_et=1&format=json&sep=1"
    proxy_ip = None
    get_ip_time = None
    rest_time = None
    count = 0
    fail_times = 0
    expire_time = "2021-01-20 15:32:08"

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
    def update_proxy_ip1(cls):
        get_result = requests.get(cls.api_url1).json()['data']['proxy_list'][0].split(",")
        proxy_ip, rest_time = get_result[0], get_result[1]
        cls.proxy_ip = proxy_ip
        logger.warning("使用了持久性个IP[%s]，剩余时间%ss" % (proxy_ip, rest_time))

    @classmethod
    def update_proxy_ip(cls):
        try:
            # res = {"msg": "", "code": 0, "data": {"count": 1, "proxy_list": ["122.4.52.220:19012,1559"], "order_left_count": 997, "dedup_count": 1}}
            get_result = requests.get(cls.api_url).json()['data']['proxy_list'][0].split(",")
            proxy_ip, rest_time = get_result[0], get_result[1]
            get_ip_time = int(time.time())
            cls.fail_times = 0
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
    def get_ip(cls):
        expire_time = time.strptime(cls.expire_time, "%Y-%m-%d %H:%M:%S")
        expire_time = int(time.mktime(expire_time))
        if int(time.time()) < expire_time:
            if cls.proxy_ip is None:
                cls.update_proxy_ip1()
            else:
                pass
        else:
            if cls.proxy_ip is None or cls.get_ip_time is None:
                cls.update_proxy_ip()
            else:
                cur_time = int(time.time())
                if cls.fail_times >= 5 or (cur_time - cls.get_ip_time >= (cls.rest_time - 1)):
                    cls.update_proxy_ip()
        username = "cs_qin"
        password = "7wl4jvhz"
        proxies = {
            "http": "http://%s:%s@%s/" % (username, password, cls.proxy_ip),
            "https": "http://%s:%s@%s/" % (username, password, cls.proxy_ip)
        }
        return proxies

    @classmethod
    def test(cls):
        expire_time = requests.get(cls.order_url).json()['data']['expire_time']
        expire_time = time.strptime(expire_time, "%Y-%m-%d %H:%M:%S")
        expire_time = int(time.mktime(expire_time))
        if int(time.time()) < expire_time:
            get_result = requests.get(cls.api_url1).json()['data']['proxy_list'][0].split(",")
            print(get_result)
            proxy_ip, rest_time = get_result[0], get_result[1]
            cls.proxy_ip = proxy_ip
            cls.rest_time = 1
            logger.warning("使用了持久性个IP[%s]，剩余时间%ss" % (proxy_ip, rest_time))