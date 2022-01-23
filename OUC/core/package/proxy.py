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
    wanbian_api_url = "http://ip.ipjldl.com/index.php/api/entry?method=proxyServer.tiqu_api_url&packid=0&fa=0&dt=0&groupid=0&fetch_key=&qty=1&time=103&port=1&format=json&ss=5&css=&dt=0&pro=%E5%B1%B1%E4%B8%9C%E7%9C%81&city=&usertype=6"
    api_url = "http://ip.51daili.com/getapi?packid=2&unkey=&tid=&qty=1&time=11&port=1&format=json&ss=5&css=&ipport=1&pro=&city=&dt=1&usertype=17"
    api_url1 = "http://csqin666.v4.dailiyun.com/query.txt?key=NP10D7BC2A&word=&count=1&rand=false&ltime=0&norepeat=true&detail=false"
    shenlong_url = "http://api.shenlongip.com/ip?key=j7tqkala&pattern=json&count=1&need=1000&protocol=2"
    tmp_shenlong_url = "http://api.shenlongip.com/ip?key=zb0thifp&pattern=json&count=1&need=1000&protocol=1"
    proxy_ip = None
    get_ip_time = None
    rest_time = None
    count = 0
    fail_times = 0
    timeout_times = 0

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
        cls.fail_times = 0
        cls.timeout_times = 0
        try:
            # 神龙ip
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
        # 神龙ip
        username = "csqin"
        password = "lichengjiahua423"
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
            if int(time.time()) - int(get_ip_time) >= int(rest_time) or force_update == 1 or cls.fail_times > 10 or cls.timeout_times > 20:
                proxy_ip = cls.update_proxy_ip(proxy_ip_info)

        proxies = {
            "http": "http://%s/" % proxy_ip,
            "https": "http://%s/" % proxy_ip
        }
        return proxies

    # 万变ip
    # res = requests.get(cls.wanbian_api_url).json()['data'][0]
    # proxy_ip = "%s:%s" % (res['IP'], res['Port'])
    # 猿人云
    # res = requests.get(cls.shenlong_url).json()['data'][0]
    # proxy_ip = "%s:%s" % (res['ip'], res['port'])
    # 51代理
    # proxy_ip = requests.get(cls.api_url).json()['data'][0]['IP']

    # 万变ip
    # username = "csqin"
    # password = "lichengjiahua423"
    # 猿人云
    # username = "2021032800001502146"
    # password = "K2eXDjBmKd0P5NQI"
    # 51代理
    # username = "csqin666"
    # password = "lichengjiahua423"

    # proxies = {
    #     "http": "http://%s:%s@%s/" % (username, password, proxy_ip),
    #     "https": "http://%s:%s@%s/" % (username, password, proxy_ip)
    # }