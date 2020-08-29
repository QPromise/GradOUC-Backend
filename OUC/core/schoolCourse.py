'''
_*_coding:utf-8 _*_

@Author  :  csqin

@Contact :  qcs@stu.ouc.edu.cn

@Software:  PyCharm

@filename:  schoolCourse.py

@Time    :  2020/1/13 16:52

@Desc    :  

'''
import base64
import requests
import pandas as pd
from bs4 import BeautifulSoup
import math
import numpy as np
import re

headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}

# 登录地址
login_url = "http://id.ouc.edu.cn:8071/sso/login?service=http%3A%2F%2Fpgs.ouc.edu.cn%2Fallogene%2Fpage%2Fhome.htm%3B"
# 登录后主页
home_url = "http://pgs.ouc.edu.cn/allogene/page/home.htm"
# 课程地址
schoolCourse_url = "http://pgs.ouc.edu.cn/py/page/teacher/lnsjCxdc.htm"


def base64encode(passwd):
    encode_passwd = base64.b64encode(passwd.encode('GBK'))  # .decode('ascii') 转换成字符形式
    return encode_passwd


def main(kkyx='-1', kcmc='', jsxm='蒋永国', pageId=1):
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
        "username": '21180231272',
        "password": base64encode('608401'),
        "lt": lt,
        "_eventId": eventId
    }

    # 提交登录表单
    post_form = session.post(url=login_url, headers=headers, data=values)
    import urllib
    # 获取登录后主页面
    home_page = session.get(url=home_url, headers=headers)
    home_soup = BeautifulSoup(home_page.text, 'lxml')
    res = {"message": "", "pages_count": "", "schoolCourses": "", "have_course": 0}
    if home_soup.findAll(name="div", attrs={"class": "panel_password"}):
        print('登录失败!')
        res["message"] = "fault"
        return res
    else:
        print('登录成功!')
        self_info = pd.read_html(home_page.text)[0]
        print(pd.DataFrame(self_info))
        res["message"] = "success"

        """
        教师姓名：jsxm
        课程名称：kcmc
        院系：kkyx
        """
        print(kkyx, kcmc, jsxm, pageId)
        param = "?operateType=search" \
                + "&key=&kckkxj=-1" \
                + "&kkyx=" + kkyx \
                + "&kcxz=-1&skyy=-1&tskc=&kcbh=" \
                + "&kcmc=" + kcmc + "&jsgh=" + "&jsxm=" + urllib.parse.unquote(
            str(urllib.parse.quote(jsxm))) + "&pageId=" + str(pageId)

        print(param)
        schoolCourse_page = session.post(schoolCourse_url + param, headers=headers)
        schoolCourse_soup = BeautifulSoup(schoolCourse_page.text, 'lxml')
        print(schoolCourse_soup)
        temp = schoolCourse_soup.findAll(name="p", attrs={"class": "w250 fr tar"})
        pre = str(temp[0]).index('共')
        post = str(temp[0]).index('个')
        res['pages_count'] = math.ceil(int(str(temp[0])[pre + 1:post]) / 20)
        print(res['pages_count'])
        schoolCourse_table = pd.read_html(schoolCourse_page.text)[0]
        schoolCourse_table = pd.DataFrame(schoolCourse_table)
        schoolCourse_table = schoolCourse_table.fillna("")
        # print(schoolCourse_table)
        schoolCourses = []
        if len(schoolCourse_table) != 0:
            for i in range(len(schoolCourse_table.values)):
                schoolCourse = {}
                schoolCourse["xn"] = schoolCourse_table[i:i + 1].values[0][0]
                schoolCourse["xq"] = schoolCourse_table[i:i + 1].values[0][1]
                schoolCourse["number"] = schoolCourse_table[i:i + 1].values[0][2]
                schoolCourse["name"] = schoolCourse_table[i:i + 1].values[0][3]
                schoolCourse["department"] = schoolCourse_table[i:i + 1].values[0][4]
                schoolCourse["credit"] = schoolCourse_table[i:i + 1].values[0][5]
                schoolCourse["period"] = schoolCourse_table[i:i + 1].values[0][6]
                schoolCourse["capacity"] = schoolCourse_table[i:i + 1].values[0][7]
                schoolCourse["teacher"] = schoolCourse_table[i:i + 1].values[0][8]
                schoolCourse["language"] = schoolCourse_table[i:i + 1].values[0][9]
                schoolCourse["campus"] = schoolCourse_table[i:i + 1].values[0][10]
                schoolCourse["info"] = schoolCourse_table[i:i + 1].values[0][11]
                schoolCourses.append(schoolCourse)
            # print(schoolCourses)
            print(len(schoolCourses))
            res['schoolCourses'] = schoolCourses
            res['have_course'] = 1
        return res


if __name__ == '__main__':
    # print(main("21190211105", ""))
    print(main())
