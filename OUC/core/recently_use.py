#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: qinchangshuai(cs_qin@qq.com) 
Date: 2021/1/17 11:11 
"""
import time

from OUC import models
from OUC import log

logger = log.logger


def get_time_gap(before):
    cur_time = int(time.time())
    time_gap = cur_time - before
    if time_gap < 60:
        res = "%s秒" % time_gap
    elif time_gap < 3600:
        res = "%s分钟" % (time_gap // 60)
    elif time_gap < 3600 * 24:
        res = "%s小时" % (time_gap // 3600)
    else:
        res = "%s天" % (time_gap // (3600 * 24))
    return res


def main():
    try:
        students = models.Student.objects.all()[:25]
        res = []
        for student in students:
            cur_info = {"url": "url", "title": ""}
            time_gap = get_time_gap(int(student.update_date.timestamp()))
            department = student.department
            name = student.name
            if department != "-":
                title = "%s的%s同学%s前访问了系统" % (department, name[0], time_gap)
            else:
                title = "中国海洋大学的某位同学%s前访问了系统" % time_gap
            cur_info["title"] = title
            res.append(cur_info)
        return {"message": "success", "use_news": res}
    except Exception as e:
        logger.log("获取最近访问小程序的同学失败: %s" % e)
        return {"message": "fault", "use_news": ""}


if __name__ == '__main__':
    print(get_time_gap(1610862466))


