#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: cs_qin(cs_qin@qq.com)
Date: 2020/8/30 22:06
"""

import pandas as pd

from OUC.core.package import login
from OUC import log

logger = log.logger

headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}

# 课程地址
course_url = "http://pgs.ouc.edu.cn/py/page/student/grkcgl.htm"


def main(sno, passwd, openid):
    res = {"message": "", "courses": "", "have_class": 0}
    login_info = login.Login.login(sno, passwd, openid)
    if login_info["message"] == "success":
        session = login_info["session"]
        res["message"] = login_info["message"]
        try:
            course_page = session.get(course_url, headers=headers)
            planned_table = pd.read_html(course_page.text)[0]
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
                res['have_class'] = 1
                return res
        except Exception as e:
            logger.error("[sno]: %s [passwd]: %s [Exception]: %s" % (sno, passwd, e))
            res['have_class'] = 2
            return res
    else:
        res["message"] = login_info["message"]
        res["have_class"] = 2
        return res


if __name__ == '__main__':
    print(main("21200231213", "", None))
