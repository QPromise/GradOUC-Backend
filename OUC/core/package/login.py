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

from OUC import models


class Login(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    }
    # 登录地址
    login_url = "http://id.ouc.edu.cn:8071/sso/login?service=http%3A%2F%2Fpgs.ouc.edu.cn%2Fallogene%2Fpage%2Fhome.htm%3B"
    new_login_url = "http://pgs.ouc.edu.cn/sso/login?service=http%3A%2F%2Fpgs.ouc.edu.cn%2Fpy%2Fpage%2Fstudent%2Fxslcsm.htm%3B"
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
            print(e)
            return None

    @classmethod
    def write_student_info(cls, username, password, session):
        student = models.Student.objects.filter(sno=username)
        if len(student) == 0:
            res = cls.get_student_info(session)
            if res is not None:
                models.Student.objects.create(sno=username, name=res["name"], passwd=password,
                                              department=res["department"], profession=res["profession"],
                                              research=res["research"], supervisor=res["supervisor"])
            else:
                models.Student.objects.create(sno=username, passwd=password)
        else:
            if student[0].name == "-":
                res = cls.get_student_info(session)
                if res is not None:
                    student.update(name=res["name"], department=res["department"], profession=res["profession"],
                                   research=res["research"], supervisor=res["supervisor"],
                                   update_date=timezone.now())
                else:
                    student.update(passwd=password, update_date=timezone.now())
            else:
                print("here")
                student.update(passwd=password, update_date=timezone.now())

    @classmethod
    def base64encode(cls, password):
        """密码加密"""
        encode_password = base64.b64encode(password.encode('GBK'))  # .decode('ascii') 转换成字符形式
        return encode_password

    @classmethod
    def login(cls, username, password):
        """登录研究生系统主页"""
        try:
            # 创建一个回话
            session = requests.Session()
            # 获得登录页面
            response = session.get(cls.login_url)
            login_soup = BeautifulSoup(response.text, 'lxml')
            # 获取隐藏字段
            lt = login_soup.form.find("input", {"name": "lt"})["value"]
            eventId = login_soup.form.find("input", {"name": "_eventId"})["value"]
            # 填写post信息
            values = {
                "username": username,
                "password": cls.base64encode(password),
                "lt": lt,
                "_eventId": eventId
            }
        except Exception as e:
            print(e)
            return {"message": "fault"}
        # 提交登录表单
        try:
            post_form = session.post(url=cls.login_url, headers=cls.headers, data=values)
            home_page = session.get(url=cls.home_url, headers=cls.headers, timeout=6)
        except Exception as e:
            print(e)
            return {"message": "timeout"}

        try:
            home_soup = BeautifulSoup(home_page.text, 'lxml')
            if home_soup.findAll(name="div", attrs={"class": "panel_password"}):
                print('登录失败!')
                return {"message": "fault"}
            else:
                print('登录成功!')
                cls.write_student_info(username, password, session)
                return {"message": "success", "session": session}
        except Exception as e:
            print(e)
            return {"message": "fault"}
