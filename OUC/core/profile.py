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


headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}

# 登录地址
login_url = "http://id.ouc.edu.cn:8071/sso/login?service=http%3A%2F%2Fpgs.ouc.edu.cn%2Fallogene%2Fpage%2Fhome.htm%3B"
new_login_url = "http://pgs.ouc.edu.cn/sso/login?service=http%3A%2F%2Fpgs.ouc.edu.cn%2Fpy%2Fpage%2Fstudent%2Fxslcsm.htm%3B"
# 登录后主页
home_url = "http://pgs.ouc.edu.cn/allogene/page/home.htm" \
           ""
# profile
profile_url = "http://pgs.ouc.edu.cn/py/page/student/ckgrxxjh.htm"


def base64encode(passwd):
    encode_passwd = base64.b64encode(passwd.encode('GBK'))  # .decode('ascii') 转换成字符形式
    return encode_passwd


def main(username='', password=''):
    # 创建一个回话
    session = requests.Session()

    # 获得登录页面
    response = session.get(login_url)
    login_soup = BeautifulSoup(response.text, 'lxml')

    # 获取隐藏字段
    lt = login_soup.form.find("input", {"name": "lt"})["value"]
    eventId = login_soup.form.find("input", {"name": "_eventId"})["value"]

    # 填写post信息
    values = {
        "username": username,
        "password": base64encode(password),
        "lt": lt,
        "_eventId": eventId
    }
    res = {"message": "", "info": "", "have_class": 0}
    try:
        # 提交登录表单
        post_form = session.post(url=login_url, headers=headers, data=values)
        # 获取登录后主页面
        res["message"] = "timeout"
        home_page = session.get(url=home_url, headers=headers, timeout=6)
        res["message"] = "fault"
        home_soup = BeautifulSoup(home_page.text, 'lxml')
        if home_soup.findAll(name="div", attrs={"class": "panel_password"}):
            print('登录失败!')
            return res
        else:
            print('登录成功!')
            try:
                res["message"] = "success"
                profile_page = session.get(profile_url, headers=headers)
                profile_soup = BeautifulSoup(profile_page.text, 'lxml')
                name = profile_soup.findAll(name="dt", attrs={"class": "title cblue"})[0].text
                # ml10 content w300
                need_list = profile_soup.findAll(name="dd", attrs={"class": "ml10 content w300"})
                profession = need_list[2].text.split("：")[1]
                research = need_list[3].text.split("：")[1]
                supervisor = need_list[4].text.split("：")[1]
                # print(name, profession, research, supervisor)
                info = {"name": name, "profession": profession, "research": research, "supervisor": supervisor}
                res["info"] = info
                res['have_info'] = 1
            except Exception as e:
                print(e)
                res['have_info'] = 2
                return res
            return res
    except Exception as e:
        print(e)
        res["have_info"] = 2
        return res


if __name__ == '__main__':
    print(main("21200231213", ""))
