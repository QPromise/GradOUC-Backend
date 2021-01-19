#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: cs_qin(cs_qin@qq.com)
Date: 2020/8/30 22:06 
"""

import base64
import requests
from bs4 import BeautifulSoup
import django.utils.timezone as timezone
import time
import threading

from OUC import models
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
            logger.info("%s生成了第%s个IP[%s]，剩余时间%ss" % (get_ip_time, cls.count, proxy_ip, rest_time))
        except Exception as e:
            logger.error("获取ip异常%s" % e)
            cls.proxy_ip = None
            cls.get_ip_time = None
            cls.rest_time = None

    @classmethod
    def get_ip(cls):
        if cls.proxy_ip is None:
            cls.update_proxy_ip()
        else:
            cur_time = int(time.time())
            if cur_time - cls.get_ip_time > cls.rest_time:
                cls.update_proxy_ip()
        return cls.proxy_ip


class Login(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        'Connection': 'close'
    }
    # 登录地址
    login_url = "http://id.ouc.edu.cn:8071/sso/login?service=http%3A%2F%2Fpgs.ouc.edu.cn%2Fallogene%2Fpage%2Fhome.htm"
    new_login_url = "http://pgs.ouc.edu.cn/sso/login?service=http%3A%2F%2Fpgs.ouc.edu.cn%2Fallogene%2Fpage%2Fhome.htm"
    # 登录后主页
    home_url = "http://pgs.ouc.edu.cn/allogene/page/home.htm"
    # profile
    profile_url = "http://pgs.ouc.edu.cn/py/page/student/ckgrxxjh.htm"

    def __init__(self):
        pass

    @classmethod
    def get_student_info(cls, session):
        try:
            profile_page = session.get(cls.profile_url, headers=cls.headers, timeout=6)
            profile_soup = BeautifulSoup(profile_page.text, 'lxml')
            name = profile_soup.findAll(name="dt", attrs={"class": "title cblue"})[0].text
            need_list = profile_soup.findAll(name="dd", attrs={"class": "ml10 content w300"})
            department = need_list[1].text.split("：")[1]
            profession = need_list[2].text.split("：")[1]
            research = need_list[3].text.split("：")[1]
            supervisor = need_list[4].text.split("：")[1]
            return {"name": name,
                    "department": department,
                    "profession": profession,
                    "research": research,
                    "supervisor": supervisor}
        except Exception as e:
            logger.error("[Exception]: %s" % e)
            return None

    @classmethod
    def write_student_info(cls, sno, passwd, openid, session):
        passwd = cls.base64encode(passwd).decode('ascii')
        student = models.Student.objects.filter(openid=openid)
        if len(student) == 0:
            res = cls.get_student_info(session)
            try:
                if res is not None:
                    models.Student.objects.create(openid=openid, sno=sno, name=res["name"], passwd=passwd,
                                                  department=res["department"], profession=res["profession"],
                                                  research=res["research"], supervisor=res["supervisor"])
                else:
                    models.Student.objects.create(openid=openid, sno=sno, passwd=passwd)
            except Exception as e:
                logger.error("[write student info repeated]: [sno]: %s [passwd]: %s [Exception]: %s" % (sno, passwd, e))
        else:
            # 如果当前openid的账号和密码没变
            if student[0].sno == sno and student[0].passwd == passwd:
                # 之前没有获取到姓名等
                if student[0].name == "-":
                    res = cls.get_student_info(session)
                    if res is not None:
                        student.update(sno=sno, passwd=passwd, name=res["name"], department=res["department"],
                                       profession=res["profession"], research=res["research"],
                                       supervisor=res["supervisor"],
                                       update_date=timezone.now())
                    # 这次也没有获取到
                    else:
                        student.update(update_date=timezone.now())
                # 之前获取到了，只更新登录时间，这个是情况最多的。
                else:
                    # print("here-----", openid)
                    student.update(update_date=timezone.now())
            # 用户换了账号密码
            else:
                res = cls.get_student_info(session)
                if res is not None:
                    student.update(sno=sno, passwd=passwd, name=res["name"], department=res["department"],
                                   profession=res["profession"], research=res["research"],
                                   supervisor=res["supervisor"], update_date=timezone.now())
                # 这次没有获取到
                else:
                    student.update(sno=sno, passwd=passwd, name="-", department="-", profession="-",
                                   research="-", supervisor="-", update_date=timezone.now())

    @classmethod
    def base64encode(cls, passwd):
        """密码加密"""
        encode_passwd = base64.b64encode(passwd.encode('GBK'))  # .decode('ascii') 转换成字符形式
        return encode_passwd

    @classmethod
    def login(cls, sno, passwd, openid):
        """登录研究生系统主页"""
        try:
            # 创建一个回话
            session = requests.Session()
            session.keep_live = False
            session.verify = False
            username = "cs_qin"
            password = "7wl4jvhz"
            proxy_ip = ProxyIP.get_ip()
            if proxy_ip is not None:
                proxies = {
                    "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
                    "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip}
                }
                session.proxies = proxies
            else:
                logger.error("获取代理ip失败")
            # 获得登录页面
            response = session.get(cls.login_url, headers=cls.headers, timeout=6)
            login_soup = BeautifulSoup(response.text, 'lxml')
            # 获取隐藏字段
            lt = login_soup.form.find("input", {"name": "lt"})["value"]
            eventId = login_soup.form.find("input", {"name": "_eventId"})["value"]
            # 填写post信息
            values = {
                "username": sno,
                "password": cls.base64encode(passwd),
                "lt": lt,
                "_eventId": eventId
            }
        except Exception as e:
            session.close()
            logger.error("[sno]: %s [passwd]: %s [Exception]: %s" % (sno, passwd, e))
            return {"message": "fault"}
        # 提交登录表单
        try:
            post_form = session.post(url=cls.login_url, headers=cls.headers, data=values)
            home_page = session.get(url=cls.home_url, headers=cls.headers, timeout=6)

        except Exception as e:
            session.close()
            logger.error("[sno]: %s [passwd]: %s [Exception]: %s" % (sno, passwd, e))
            return {"message": "timeout"}
        try:
            home_soup = BeautifulSoup(home_page.text, 'lxml')
            if home_soup.findAll(name="div", attrs={"class": "panel_password"}):
                session.close()
                logger.error("[sno]: %s [passwd]: %s [Exception]: %s" % (sno, passwd, "登录失败！"))
                return {"message": "fault"}
            else:
                if openid is not None and openid != "null":
                    cls.write_student_info(sno, passwd, openid, session)
                else:
                    pass
                return {"message": "success", "session": session}
        except Exception as e:
            session.close()
            logger.error("[sno]: %s [passwd]: %s [Exception]: %s" % (sno, passwd, e))
            return {"message": "fault"}
