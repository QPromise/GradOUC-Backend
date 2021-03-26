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
    # https://kps.kdlapi.com/api/getkps/?orderid=911173601436870&num=1&pt=1&f_et=1&format=json&sep=1
    api_url = "http://a.ipjldl.com/getapi?packid=1&unkey=&tid=&qty=1&time=2&port=1&format=json&ss=5&css=&ipport=1&pro=&city=&dt=1&usertype=17"
    api_url1 = "http://csqin666.v4.dailiyun.com/query.txt?key=NP10D7BC2A&word=&count=1&rand=false&ltime=0&norepeat=true&detail=false"
    proxy_ip = None
    get_ip_time = None
    rest_time = None
    count = 0
    fail_times = 0

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
            get_result = requests.get(cls.api_url).json()['data'][0]['IP']
            logger.info("获取的ip为%s" % get_result)
            # get_result = requests.get(cls.api_url1).text.replace("\n", "").replace("\r", "")
            proxy_ip, rest_time = get_result, 59
            get_ip_time = int(time.time())
            cls.proxy_ip = proxy_ip
            cls.rest_time = int(rest_time)
            cls.get_ip_time = get_ip_time
            logger.warning("使用了IP[%s]，获取时间%ss, 剩余时间%ss" % (proxy_ip, get_ip_time, rest_time))
        except Exception as e:
            logger.error("%s, %s" % (e, requests.get(cls.api_url).text))

    @classmethod
    def get_ip(cls):
        if cls.proxy_ip is None:
            cls.update_proxy_ip()
        else:
            cur_time = int(time.time())
            if cur_time - cls.get_ip_time >= cls.rest_time:
                cls.update_proxy_ip()
        username = "csqin666"
        password = "lichengjiahua423"
        proxies = {
            "http": "http://%s:%s@%s/" % (username, password, cls.proxy_ip),
            "https": "http://%s:%s@%s/" % (username, password, cls.proxy_ip)
        }
        # print(proxies)
        return proxies

    # @classmethod
    # def update_proxy_ip(cls):
    #     get_result = requests.get(cls.api_url).json()['data']['proxy_list'][0].split(",")
    #     proxy_ip, rest_time = get_result[0], get_result[1]
    #     get_ip_time = int(time.time())
    #     cls.proxy_ip = proxy_ip
    #     cls.rest_time = int(rest_time)
    #     cls.get_ip_time = get_ip_time
    #     logger.warning("使用了持久性个IP[%s]，获取时间%ss, 剩余时间%ss" % (proxy_ip, get_ip_time, rest_time))
    #
    # @classmethod
    # def get_ip(cls):
    #     if cls.proxy_ip is None:
    #         cls.update_proxy_ip()
    #     else:
    #         cur_time = int(time.time())
    #         if cur_time - cls.get_ip_time >= cls.rest_time:
    #             cls.update_proxy_ip()
    #     username = "cs_qin"
    #     password = "7wl4jvhz"
    #     proxies = {
    #         "http": "http://%s:%s@%s/" % (username, password, cls.proxy_ip),
    #         "https": "http://%s:%s@%s/" % (username, password, cls.proxy_ip)
    #     }
    #     return proxies

    # @classmethod
    # def update_proxy_ip(cls):
    #     try:
    #         # res = {"msg": "", "code": 0, "data": {"count": 1, "proxy_list": ["122.4.52.220:19012,1559"], "order_left_count": 997, "dedup_count": 1}}
    #         get_result = requests.get(cls.api_url).json()['data']['proxy_list'][0].split(",")
    #         proxy_ip, rest_time = get_result[0], get_result[1]
    #         get_ip_time = int(time.time())
    #         cls.fail_times = 0
    #         cls.proxy_ip = proxy_ip
    #         cls.rest_time = int(rest_time)
    #         cls.get_ip_time = get_ip_time
    #         cls.count += 1
    #         logger.warning("%s生成了第%s个IP[%s]，剩余时间%ss" % (get_ip_time, cls.count, proxy_ip, rest_time))
    #     except Exception as e:
    #         logger.error("获取ip异常%s" % e)
    #         cls.proxy_ip = None
    #         cls.get_ip_time = None
    #         cls.rest_time = None

    # @classmethod
    # def test(cls):
    #     expire_time = time.strptime(cls.expire_time, "%Y-%m-%d %H:%M:%S")
    #     expire_time = int(time.mktime(expire_time))
    #     if int(time.time()) < expire_time:
    #         if cls.proxy_ip is None:
    #             cls.update_proxy_ip1()
    #         else:
    #             pass
    #     else:
    #         if cls.proxy_ip is None or cls.get_ip_time is None:
    #             cls.update_proxy_ip()
    #         else:
    #             cur_time = int(time.time())
    #             if cls.fail_times >= 5 or (cur_time - cls.get_ip_time >= (cls.rest_time - 1)):
    #                 cls.update_proxy_ip()
    #     username = "cs_qin"
    #     password = "7wl4jvhz"
    #     proxies = {
    #         "http": "http://%s:%s@%s/" % (username, password, cls.proxy_ip),
    #         "https": "http://%s:%s@%s/" % (username, password, cls.proxy_ip)
    #     }
    #     return proxies