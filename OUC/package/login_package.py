#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: cs_qin(cs_qin@qq.com)
Date: 2020/8/30 22:06 
"""

import base64
import requests
import pandas as pd
from bs4 import BeautifulSoup


class Login(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    }
    # 登录地址
    login_url = "http://id.ouc.edu.cn:8071/sso/login?service=http%3A%2F%2Fpgs.ouc.edu.cn%2Fallogene%2Fpage%2Fhome.htm%3B"
    new_login_url = "http://pgs.ouc.edu.cn/sso/login?service=http%3A%2F%2Fpgs.ouc.edu.cn%2Fpy%2Fpage%2Fstudent%2Fxslcsm.htm%3B"

    def __init__(self):
        pass

    @classmethod
    def base64encode(cls, password):
        """密码加密"""
        encode_password = base64.b64encode(password.encode('GBK'))  # .decode('ascii') 转换成字符形式
        return encode_password

    @classmethod
    def login(cls, username, password):
        """登录研究生系统主页"""
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

        # 提交登录表单
        post_form = session.post(url=cls.login_url, headers=cls.headers, data=values)
        return session
