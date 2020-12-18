#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: cs_qin(cs_qin@qq.com)
Date: 2020/8/30 22:06
"""

import pandas as pd
from bs4 import BeautifulSoup
import math

from OUC.core.package import login
from OUC import log

logger = log.logger

headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
}

# 课程地址
school_course_url = "http://pgs.ouc.edu.cn/py/page/student/lnsjCxdc.htm"


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


def main(xn, xq, sno, passwd, openid, kkyx=-1, kcmc='', jsxm='', pageId=1):
    """
    教师姓名：jsxm
    课程名称：kcmc
    院系：kkyx
    """
    res = {"message": "", "pages_count": "", "number": 0, "school_courses": "", "have_course": 0}
    login_info = login.Login.login(sno, passwd, openid)
    if login_info["message"] == "success":
        session = login_info["session"]
        res["message"] = login_info["message"]
        try:
            param = "?operateType=search&key=&kkxn=%d&kckkxj=%d&kkyx=%s" \
                    "&kcxz=%d&skyy=%d&tskc=&kcbh=&kcmc=%s&jsgh=&jsxm=%s&pageId=%d" \
                    % (int(xn), int(xq), kkyx, -1, -1, kcmc, jsxm, int(pageId))
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
                    school_course = dict()
                    school_course["xn"] = school_course_table[i:i + 1].values[0][0]
                    school_course["xq"] = school_course_table[i:i + 1].values[0][1]
                    school_course["id"] = school_course_table[i:i + 1].values[0][2]
                    school_course["name"] = school_course_table[i:i + 1].values[0][3]
                    school_course["department"] = school_course_table[i:i + 1].values[0][4]
                    school_course["capacity"] = school_course_table[i:i + 1].values[0][5]
                    school_course["language"] = school_course_table[i:i + 1].values[0][6]
                    if len(school_course_table[i:i + 1].values[0][7]) <= 3 or \
                            is_all_en(school_course_table[i:i + 1].values[0][7]):
                        school_course["teacher"] = school_course_table[i:i + 1].values[0][7]
                    else:
                        school_course["teacher"] = get_no_repeat_name(school_course_table[i:i + 1].values[0][7])
                    school_course["campus"] = school_course_table[i:i + 1].values[0][8]
                    school_course["info"] = school_course_table[i:i + 1].values[0][9]
                    school_courses.append(school_course)
                res['school_courses'] = school_courses
                res['have_course'] = 1
                return res
        except Exception as e:
            logger.error("[sno]: %s [passwd]: %s [Exception]: %s" % (sno, passwd, e))
            res['have_course'] = 2
            return res
    else:
        res["message"] = login_info["message"]
        res["have_class"] = 2
        return res


if __name__ == '__main__':
    # print(main("21190211105", ""))
    pass
