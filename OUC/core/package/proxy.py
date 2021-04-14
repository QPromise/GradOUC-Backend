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
from OUC import models


logger = log.logger


class ProxyIP(object):
    _instance_lock = threading.Lock()
    api_url = "http://a.ipjldl.com/getapi?packid=2&unkey=&tid=&qty=1&time=11&port=1&format=json&ss=5&css=&ipport=1&pro=&city=&dt=1&usertype=17"
    api_url1 = "http://csqin666.v4.dailiyun.com/query.txt?key=NP10D7BC2A&word=&count=1&rand=false&ltime=0&norepeat=true&detail=false"
    shenlong_url = "https://tunnel-api.apeyun.com/d?id=2021032800001502146&secret=K2eXDjBmKd0P5NQI&limit=1&format=json&auth_mode=hand&min=3"
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
    def update_proxy_ip(cls, proxy_ip_info=None):
        try:
            # proxy_ip = requests.get(cls.api_url).json()['data'][0]['IP']
            res = requests.get(cls.shenlong_url).json()['data'][0]
            proxy_ip = "%s:%s" % (res['ip'], res['port'])
            logger.info("获取的ip为%s" % proxy_ip)
            get_ip_time = int(time.time())
            if proxy_ip_info is None:
                models.IPProxy.objects.create(proxy_ip=proxy_ip, get_ip_time=get_ip_time)
                logger.warning("首次获取IP[%s]，更新时间%ss" % (proxy_ip, get_ip_time))
            else:
                proxy_ip_info.proxy_ip = proxy_ip
                proxy_ip_info.get_ip_time = get_ip_time
                proxy_ip_info.save()
                logger.warning("更新了IP[%s]，更新时间%ss, 剩余时间%ss" % (proxy_ip, get_ip_time, proxy_ip_info.rest_time))
            return proxy_ip
        except Exception as e:
            logger.error(e)

    @classmethod
    def get_ip(cls):
        # username = "csqin666"
        # password = "lichengjiahua423"
        username = "2021032800001502146"
        password = "K2eXDjBmKd0P5NQI"
        proxy_ip_infos = models.IPProxy.objects.all()
        has_proxy_ip = len(proxy_ip_infos)
        if not has_proxy_ip:
            proxy_ip = cls.update_proxy_ip()
        else:
            proxy_ip_info = proxy_ip_infos[0]
            proxy_ip = proxy_ip_info.proxy_ip
            get_ip_time = proxy_ip_info.get_ip_time
            rest_time = proxy_ip_info.rest_time
            force_update = proxy_ip_info.force_update
            if int(time.time()) - int(get_ip_time) >= int(rest_time) or force_update == 1:
                proxy_ip = cls.update_proxy_ip(proxy_ip_info)

        proxies = {
            "http": "http://%s:%s@%s/" % (username, password, proxy_ip),
            "https": "http://%s:%s@%s/" % (username, password, proxy_ip)
        }
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