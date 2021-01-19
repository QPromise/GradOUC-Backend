#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: cs_qin(cs_qin@qq.com)
Date: 2020/8/30 22:06
"""

import pandas as pd
from bs4 import BeautifulSoup

from OUC.core.package import login
from OUC import log

logger = log.logger

headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Connection': 'close'
}

# 课程地址
course_url = "http://pgs.ouc.edu.cn/py/page/student/grkcgl.htm"


def main(sno, passwd, openid):
    res = {"message": "", "courses": "", "unplanned_courses": [], "have_class": 0,
           "school_require_credit": "--", "select_credit": "--", "get_credit": "--"}
    login_info = login.Login.login(sno, passwd, openid)
    if login_info["message"] == "success":
        session = login_info["session"]
        res["message"] = login_info["message"]
        try:
            course_page = session.get(course_url, headers=headers, timeout=12)
            session.close()
            course_soup = BeautifulSoup(course_page.text, 'lxml')
            course_table = pd.read_html(course_page.text)
            credits = course_soup.findAll(name="dd")
            # 学校要求培养方案学分
            try:
                school_require_credit = credits[8].text
                # 你选课的学分
                select_credit = credits[9].text
                # 已获得的学分
                get_credit = credits[10].text
            except Exception as e:
                school_require_credit, select_credit, get_credit = "--", "--", "--"
                logger.error("[sno]: %s [passwd]: %s [Exception]: %s" % (sno, passwd, e))
            # 计划内的课程
            planned_table = course_table[0]
            planned_table = pd.DataFrame(planned_table)
            planned_table = planned_table.fillna("")
            planned_courses = []
            if len(planned_table) != 0:
                for i in range(len(planned_table.values)):
                    planned_course = {"select": "", "id": "", "name": "", "type": "",
                                      "credit": None, "xn": "", "xq": "", "teacher": "", "process": ""}
                    planned_course["select"] = planned_table[i:i + 1].values[0][0]
                    planned_course["id"] = planned_table[i:i + 1].values[0][1]
                    planned_course["name"] = planned_table[i:i + 1].values[0][2]
                    planned_course["type"] = planned_table[i:i + 1].values[0][3]
                    planned_course["credit"] = planned_table[i:i + 1].values[0][4]
                    planned_course["xn"] = planned_table[i:i + 1].values[0][5]
                    planned_course["xq"] = planned_table[i:i + 1].values[0][6]
                    planned_course["teacher"] = planned_table[i:i + 1].values[0][7]
                    planned_course["process"] = planned_table[i:i + 1].values[0][8]
                    planned_courses.append(planned_course)
                res['courses'] = planned_courses
                res['school_require_credit'] = school_require_credit
                res['select_credit'] = select_credit
                res['get_credit'] = get_credit
                res['have_class'] = 1
            # 如果有计划外的课程
            if len(course_table) > 1:
                unplanned_table = course_table[1]
                unplanned_table = pd.DataFrame(unplanned_table)
                unplanned_table = unplanned_table.fillna("")
                unplanned_courses = []
                if len(unplanned_table) != 0:
                    for i in range(len(unplanned_table.values)):
                        unplanned_course = {"select": "", "id": "", "name": "", "type": "",
                                          "credit": None, "xn": "", "xq": "", "teacher": "", "process": ""}
                        unplanned_course["select"] = unplanned_table[i:i + 1].values[0][0]
                        unplanned_course["id"] = unplanned_table[i:i + 1].values[0][1]
                        unplanned_course["name"] = unplanned_table[i:i + 1].values[0][2]
                        unplanned_course["type"] = unplanned_table[i:i + 1].values[0][3]
                        unplanned_course["credit"] = unplanned_table[i:i + 1].values[0][4]
                        unplanned_course["xn"] = unplanned_table[i:i + 1].values[0][5]
                        unplanned_course["xq"] = unplanned_table[i:i + 1].values[0][6]
                        unplanned_course["teacher"] = unplanned_table[i:i + 1].values[0][7]
                        unplanned_course["process"] = unplanned_table[i:i + 1].values[0][8]
                        unplanned_courses.append(unplanned_course)
                    res['unplanned_courses'] = unplanned_courses
            return res
        except Exception as e:
            session.close()
            logger.error("[sno]: %s [passwd]: %s [Exception]: %s" % (sno, passwd, e))
            res['have_class'] = 2
            return res
    else:
        res["message"] = login_info["message"]
        res["have_class"] = 2
        return res


if __name__ == '__main__':
    print(main("21201631055", "", None))
    print(main("21200231213", "", None))
