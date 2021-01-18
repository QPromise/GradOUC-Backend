#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: qinchangshuai(cs_qin@qq.com) 
Date: 2020/12/26 21:34 
"""

import pandas as pd
import numpy as np
import re
import collections

from OUC.core.package import login
from OUC import log

logger = log.logger

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}

# 课表地址
schedule_url = "http://pgs.ouc.edu.cn/py/page/student/grkcb.htm"
days = {'0': "星期一", '1': "星期二", '2': "星期三", '3': "星期四", '4': "星期五", '5': "星期六", '6': "星期日"}
courses_time = ["08:00-08:50", "09:00-09:50", "10:10-11:00", "11:10-12:00",
                "13:30-14:20", "14:30-15:20", "15:30-16:20", "16:30-17:20",
                "17:30-18:20", "18:30-19:20", "19:30-20:20", "20:30-21:20"
                ]


def main(sno, passwd, openid, zc, xj, xn, day):
    res = {"message": "", "course": ""}
    login_info = login.Login.login(sno, passwd, openid)
    if login_info["message"] == "success":
        session = login_info["session"]
        res["message"] = login_info["message"]
        try:
            param = "?zc=" + str(zc) + "&xj=" + str(xj) + "&xn=" + str(xn)
            schedule_page = session.get(url=schedule_url + param, headers=headers, timeout=6)
            session.close()
            # print(schedule_page.text)
            # 我的课程表
            courses_table = pd.read_html(schedule_page.text)[0]
            # 要看第几天的课程
            courses_info = courses_table[days[day]].values
            courses_info = pd.DataFrame(courses_info).fillna('')
            courses_info = np.array(courses_info)
            courses_info = courses_info.T.tolist()[0]
            # courses_info = ['', '', '', '', '', '专业学位研究生外国语 || ( 4-6,8-9 )周  第2节 -- 第4节 高国栋 7201', '', '', '',
            #                 '专业学位研究生外国语 || ( 4-6,8-9 )周  第2节 -- 第4节 高国栋 7101', '', '']
            # print(courses_info)
            day_courses = collections.OrderedDict()
            for i in range(len(courses_info)):
                cur_course_info = dict()
                if courses_info[i] == '':
                    pass
                else:
                    cur_course_split = courses_info[i].split()
                    name = cur_course_split[0]
                    room = cur_course_split[-1]
                    course_key = "%s+%s" % (name, room)
                    if day_courses.get(course_key, None) is None:
                        cur_course_info["name"] = name
                        cur_course_info["room"] = room
                        cur_course_info["span"] = [i]
                        day_courses[course_key] = cur_course_info
                    else:
                        day_courses[course_key]["span"].append(i)
            courses = []
            for k, v in day_courses.items():
                course = dict()
                course["name"] = v["name"]
                course["room"] = v["room"]
                span_list = v["span"]
                begin = min(span_list)
                end = max(span_list)
                if begin == end:
                    span = "%s" % (begin + 1)
                elif end - begin == len(span_list) - 1:
                    span = "%s-%s" % (begin + 1, end + 1)
                else:
                    span = "%s" % ",".join(list(map(str, [ele + 1 for ele in span_list])))
                course["span"] = span
                course["time_begin"] = courses_time[span_list[0]].split("-")[0]
                course["time_end"] = courses_time[span_list[-1]].split("-")[-1]
                courses.append(course)
            res['course'] = courses
            return res
        except Exception as e:
            logger.error("[sno]: %s [passwd]: %s [Exception]: %s" % (sno, passwd, e))
            res["message"] = "timeout"
            return res
    else:
        res["message"] = login_info["message"]
        return res

# """
# 以下课程时间地点待定,具体请关注课程备注或相关通知：
# """
# undetermined_table = pd.read_html(schedule_page.text)[1]
# undetermined_schedule = pd.DataFrame(undetermined_table)
# undetermined_schedule = undetermined_schedule.fillna('no_info')
# print(undetermined_schedule)
# undetermined_schedule.to_csv(r'store.csv', mode='a', encoding='utf_8_sig')


if __name__ == '__main__':
    # main("", "", "null", "17", "11", "2020")
    main("21200231213", "", "", "16", "11", "2020", 4)
