#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: cs_qin(cs_qin@qq.com)
Date: 2020/8/30 22:06
"""

import pandas as pd
import numpy as np
import re
import time

from OUC.core.package import login
from OUC import log

logger = log.logger

headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Connection': 'close'
}

# 课程地址
course_url = "http://pgs.ouc.edu.cn/py/page/student/grkcgl.htm"


def calculate_score(score, credit):
    return round(np.sum(np.array(score) * np.array(credit)) / np.sum(np.array(credit)), 4)


def main(sno, passwd, openid):
    res = {"message": "", "courses": "", "mean": "", "have_class": 0}
    login_info = login.Login.login(sno, passwd, openid)
    if login_info["message"] == "success":
        session = login_info["session"]
        res["message"] = login_info["message"]
        try:
            course_page = session.get(course_url, headers=headers, timeout=6)
            session.close()
            # 计划内的课程
            planned_table = pd.read_html(course_page.text)[0]
            planned_table = pd.DataFrame(planned_table)
            planned_table = planned_table.fillna("")
            planned_courses = []
            scores = []
            credits = []
            if len(planned_table) != 0:
                for i in range(len(planned_table.values)):
                    planned_course = {"name": "", "type": "", "credit": None, "score": None, "selected": False, "disabled": True}
                    planned_course["name"] = planned_table[i:i + 1].values[0][2]
                    planned_course["type"] = planned_table[i:i + 1].values[0][3]
                    planned_course["credit"] = planned_table[i:i + 1].values[0][4]
                    # planned_course["teacher"] = planned_table[i:i + 1].values[0][7]
                    process = planned_table[i:i + 1].values[0][8]
                    # 成绩出了
                    if re.search(r"(\d+)", process):
                        # 判断是否重修
                        if process.find("重修") != -1:
                            score = float(process.split()[1][1:])
                        else:
                            score = float(process.split()[2])
                        # 如果成绩大于70才计算Mean
                        if score >= 70:
                            scores.append(score)
                            credits.append(planned_course["credit"])
                            planned_course["selected"] = True
                            planned_course["disabled"] = False
                    # 成绩没出
                    else:
                        # 选了的课
                        if process.find("未选") != -1:
                            score = "未选"
                        elif process.find("免修") != -1:
                            score = "免修"
                        else:
                            score = "未出"
                    planned_course["score"] = score
                    planned_courses.append(planned_course)
                if scores != [] and credits != []:
                    res["mean"] = calculate_score(scores, credits)
                else:
                    res["mean"] = 0
                    # print("当前没有可计算的课程")
                res['courses'] = planned_courses
                res['have_class'] = 1
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
    start = time.time()
    print(main("21200231213", "", "null"))
    end = time.time()
    print(end - start)
