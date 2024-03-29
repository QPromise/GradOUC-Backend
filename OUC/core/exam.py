#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: qinchangshuai(cs_qin@qq.com) 
Date: 2021/1/16 10:32 
"""

import os
import json

from OUC.core.package import login
from OUC import log

logger = log.logger


def main(sno, my_sno, my_passwd, my_openid):
    sno = str(sno)
    res = {"message": "success", "exams": []}
    exams = []
    tmp_exams = []
    files_name = os.listdir("OUC/static/exam_json/")
    try:
        for file_name in files_name:
            # 查看json文件中是否有自己的课程
            with open('OUC/static/exam_json/' + file_name, 'r') as f:
                cur_exam = json.load(fp=f)
                for key in cur_exam:
                    if sno in cur_exam[key]:
                        tmp_exams.append(cur_exam[key][sno])
        if len(tmp_exams) == 0:
            res["message"] = "empty"
            return res
        for tmp_exam in tmp_exams:
            exam = dict()
            exam["sno"] = tmp_exam[0]
            exam["department"] = tmp_exam[1]
            exam["profession"] = tmp_exam[2]
            exam["course_num"] = tmp_exam[3]
            exam["course_name"] = tmp_exam[4]
            exam["area"] = tmp_exam[5]
            exam["room_num"] = tmp_exam[6]
            exam["seat_num"] = tmp_exam[7]
            exam["build"] = tmp_exam[8]
            exam["room"] = tmp_exam[9]
            exam["time"] = tmp_exam[10]
            exams.append(exam)
        res["exams"] = exams
        return res
    except Exception as e:
        logger.error("%s获取考试信息异常: %s" % (sno, e))
        res["message"] = "fault"
        return res

if __name__ == '__main__':
    main("21211011015", 0, 0, 0)
