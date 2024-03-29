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
from OUC.global_config import headers, course_url

logger = log.logger


def calculate_score(score, credit):
    return round(np.sum(np.array(score) * np.array(credit)) / np.sum(np.array(credit)), 4)


def main(sno, passwd, openid):
    res = {"message": "", "courses": "", "mean": "", "can_join_rank": 1, "have_class": 0}
    login_info = login.Login.login(sno, passwd, openid)
    if login_info["message"] == "success":
        session = login_info["session"]
        res["message"] = login_info["message"]
        try:
            course_page = session.get(course_url, headers=headers, timeout=8)
            session.close()
            # 计划内的课程
            planned_table = pd.read_html(course_page.text)[0]
            planned_table = pd.DataFrame(planned_table)
            planned_table = planned_table.fillna("")
            planned_courses = []
            scores = []
            credits = []
            can_join_rank = 1
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
                        # 判断是否重修，有成绩的话是可以参与排名的
                        if process.find("重修") != -1:
                            process_split = process.split()
                            if len(process_split) == 3:
                                score = float(process_split[2])
                            else:
                                score = float(process_split[1][1:])
                        else:
                            process_split = process.split()
                            get_score = re.findall(r"\d+\.?\d*", process_split[2])
                            if len(get_score) == 0:
                                get_score = re.findall(r"\d+\.?\d*", process_split[1])
                                score = float(get_score[0])
                            else:
                                score = float(process_split[2])

                        # 如果成绩大于70或者是低于70已经获得学分才计算Mean
                        if score >= 70 or process.find("已获得学分") != -1:
                            scores.append(score)
                            credits.append(planned_course["credit"])
                            planned_course["selected"] = True
                            planned_course["disabled"] = False
                        else:
                            can_join_rank = 0
                    # 成绩没有分数
                    else:
                        # 选了的课
                        if process.find("未选") != -1:
                            score = "未选"
                        elif process.find("重修") != -1:
                            # 存在没出成绩的重修科目是不能参与排名的
                            score = "重修"
                            can_join_rank = 0
                        elif process.find("免修") != -1:
                            score = "免修"
                        elif process.find("优秀") != -1:
                            score = "优秀"
                        elif process.find("良好") != -1:
                            score = "良好"
                        elif process.find("及格") != -1:
                            score = "及格"
                        elif process.find("通过") != -1:
                            score = "通过"
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
                res['can_join_rank'] = can_join_rank
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
    print(main("21210213302", "yhl123456", "null"))
    print(main("21200231213", "2020wangjie", "null"))
    end = time.time()
    print(end - start)
