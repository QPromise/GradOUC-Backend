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
import math


headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
}

# 登录地址
login_url = "http://id.ouc.edu.cn:8071/sso/login?service=http%3A%2F%2Fpgs.ouc.edu.cn%2Fallogene%2Fpage%2Fhome.htm%3B"
# 登录后主页
home_url = "http://pgs.ouc.edu.cn/allogene/page/home.htm"
# 课程地址
school_course_url = "http://pgs.ouc.edu.cn/py/page/student/lnsjCxdc.htm"


def base64encode(passwd):
    encode_passwd = base64.b64encode(passwd.encode('GBK'))  # .decode('ascii') 转换成字符形式
    return encode_passwd


def get_no_repeat_name(name):
    begin = name[0]
    for i in range(1, len(name)):
        if name[i] == begin:
            return name[:i]
    return name


def is_all_en(name):
    for ch in name:
        if ord(ch) > 255:
            return False
    return True


def main(xn, xq, sno, passwd, kkyx=-1, kcmc='', jsxm='', pageId=1):
    """
    教师姓名：jsxm
    课程名称：kcmc
    院系：kkyx
    """
    # 创建一个会话
    session = requests.Session()

    # 获得登录页面
    response = session.get(login_url)
    login_soup = BeautifulSoup(response.text, 'lxml')

    # 获取隐藏字段
    lt = login_soup.form.find("input", {"name": "lt"})["value"]
    eventId = login_soup.form.find("input", {"name": "_eventId"})["value"]
    # 填写post信息
    values = {
        "username": sno,
        "password": base64encode(passwd),
        "lt": lt,
        "_eventId": eventId
    }
    res = {"message": "", "pages_count": "", "number": 0, "school_courses": "", "have_course": 0}
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
                # self_info = pd.read_html(home_page.text)[0]
                # print(pd.DataFrame(self_info))
                print(kkyx, kcmc, jsxm, pageId)
                param = "?operateType=search&key=&kkxn=%d&kckkxj=%d&kkyx=%s" \
                        "&kcxz=%d&skyy=%d&tskc=&kcbh=&kcmc=%s&jsgh=&jsxm=%s&pageId=%d" \
                        % (int(xn), int(xq), kkyx, -1, -1, kcmc, jsxm, int(pageId))
                print(school_course_url + param)
                school_course_page = session.get(school_course_url + param, headers=headers, timeout=6)
                school_course_soup = BeautifulSoup(school_course_page.text, 'lxml')
                # 拿到个数
                temp = school_course_soup.findAll(name="p", attrs={"class": "w250 fr tar"})
                pre = str(temp[0]).index('共')
                post = str(temp[0]).index('个')
                number = int(str(temp[0])[pre + 1:post])
                res["number"] = number
                res['pages_count'] = math.ceil(number / 20)
                school_course_table = pd.read_html(school_course_page.text)[0]
                school_course_table = pd.DataFrame(school_course_table)
                school_course_table = school_course_table.fillna("")
                school_courses = []
                if len(school_course_table) != 0:
                    for i in range(len(school_course_table.values)):
                        school_course = {}
                        school_course["xn"] = school_course_table[i:i + 1].values[0][0]
                        school_course["xq"] = school_course_table[i:i + 1].values[0][1]
                        school_course["id"] = school_course_table[i:i + 1].values[0][2]
                        school_course["name"] = school_course_table[i:i + 1].values[0][3]
                        school_course["department"] = school_course_table[i:i + 1].values[0][4]
                        school_course["capacity"] = school_course_table[i:i + 1].values[0][5]
                        school_course["language"] = school_course_table[i:i + 1].values[0][6]
                        if len(school_course_table[i:i + 1].values[0][7]) <= 3 or\
                                is_all_en(school_course_table[i:i + 1].values[0][7]):
                            school_course["teacher"] = school_course_table[i:i + 1].values[0][7]
                        else:
                            school_course["teacher"] = get_no_repeat_name(school_course_table[i:i + 1].values[0][7])
                        school_course["campus"] = school_course_table[i:i + 1].values[0][8]
                        school_course["info"] = school_course_table[i:i + 1].values[0][9]
                        # print(school_course)
                        school_courses.append(school_course)
                    res['school_courses'] = school_courses
                    res['have_course'] = 1
            except Exception as e:
                print(e)
                res['have_course'] = 2
                return res
            return res
    except Exception as e:
        print(e)
        res["have_course"] = 2
        return res


if __name__ == '__main__':
    # print(main("21190211105", ""))
    pass
