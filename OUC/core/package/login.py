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

from OUC import models
from OUC import log
from OUC.core.package import proxy
from OUC.global_config import headers, home_url, login_url, profile_url

logger = log.logger


class Login(object):

    def __init__(self):
        pass

    @classmethod
    def get_student_info(cls, session):
        try:
            profile_page = session.get(profile_url, headers=headers, timeout=8)
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
            # cur_hour = datetime.datetime.now().strftime('%H:%M')
            # if cur_hour <= '01:30' or cur_hour >= '06:00':
            #     session.proxies = proxy.ProxyIP.get_ip()
            # else:
            #     proxy.ProxyIP.checkout_ip()
            # 创建一个回话
            session = requests.Session()
            session.verify = False
            session.keep_alive = False
            session.proxies = proxy.ProxyIP.get_ip()
            # 获得登录页面
            response = session.get(login_url, headers=headers, timeout=8)
            # print(response)
            login_soup = BeautifulSoup(response.text, 'lxml')
            # 获取隐藏字段
            # print(login_soup, login_soup.form)
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
            # time.sleep(1)
            post_form = session.post(url=login_url, headers=headers, timeout=8, data=values)
            home_page = session.get(url=home_url, headers=headers, timeout=8)

        except Exception as e:
            session.close()
            logger.error("[sno]: %s [passwd]: %s [Exception]: %s" % (sno, passwd, e))
            return {"message": "timeout"}
        try:
            home_soup = BeautifulSoup(home_page.text, 'lxml')
            if home_soup.findAll(name="div", attrs={"class": "panel_password"}):
                session.close()
                logger.info("[sno]: %s [passwd]: %s [Exception]: %s" % (sno, passwd, "登录失败！"))
                return {"message": "incorrect"}
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
