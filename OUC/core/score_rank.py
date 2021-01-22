#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: qinchangshuai(cs_qin@qq.com) 
Date: 2021/1/22 13:35 
"""
import requests
import json
import time
import threading
import base64
import re
import django.utils.timezone as timezone
from django.db.models import Q

from OUC import models
from OUC.core import score
from OUC import log

logger = log.logger

openid = ""
sno = ""
passwd = ""


class ScoreRank(object):

    @classmethod
    def get_my_department_profession(cls):
        pass

    @classmethod
    def set_rank_profession(cls):
        pass

    @classmethod
    def update_my_score(cls, openid, sno, passwd):
        res = cls.score_update(sno, passwd, openid, True)
        return res

    @classmethod
    def get_my_score_rank(cls, openid, sno, passwd):
        # 判断是否存在 openid sno passwd
        try:
            config = models.Config.objects.all()[0]
            sno_prefix = sno[:4]
            # 找出已经订阅的student
            if int(sno_prefix) in range(int(config.score_rank_min), int(config.score_rank_max) + 1):
                res = cls.score_update(sno, passwd, openid, False)
                if res["message"] == "success":
                    student = models.StudentRank.objects.filter(openid=openid)
                    research_list = cls.__str_to_list(str, student[0].rank_research)
                    # 同年级 同选择研究方向的人数
                    all_people = models.StudentRank.objects.filter(Q(sno__startswith=sno_prefix) & Q(research__in=research_list)).count()
                    # 同年级 选择研究方向范围内比自己分高的人数
                    rank_list = models.StudentRank.objects.filter(Q(sno__startswith=sno_prefix) & Q(research__in=research_list) & Q(avg_score__gte=student[0].avg_score)).exclude(openid=openid)
                    # 相同分数的人数
                    same_people_list = models.StudentRank.objects.filter(Q(sno__startswith=sno_prefix) & Q(research__in=research_list) & Q(avg_score=student[0].avg_score)).exclude(openid=openid)
                    same_people = len(same_people_list)
                    rank = len(rank_list) + 1
                    rank_rate = round(rank / all_people, 4)
                    add_same_rank = rank + same_people
                    add_same_rank_rate = round(add_same_rank / all_people, 4)
                    return {"message": "success", "rank": rank, "rank_rate": rank_rate, "add_same_rank": add_same_rank, "add_same_rank_rate": add_same_rank_rate, "same_people": same_people, "all_people": all_people}
                else:
                    return {"message": "fault"}
            else:
                return {"message": "illegal"}
        except Exception as e:
            logger.error(
                "[get my rank fail]: [sno]: %s [passwd]: %s [Exception]: %s"
                % (sno, passwd, e))
            return {"message": "fault"}

    @classmethod
    def score_update(cls, sno, passwd, openid, is_update_score):
        res = {"message": "success", "times": 0}
        try:
            rank_student = models.StudentRank.objects.filter(openid=openid)
            login_student = models.Student.objects.filter(openid=openid)
            if len(rank_student) == 0:
                get_score = score.main(sno, passwd, "null")
                if get_score["message"] == "success" and get_score["have_class"] == 1:
                    avg_score = get_score["mean"]
                else:
                    logger.error(
                        "[student avg_score update fail]: [sno]: %s [passwd]: %s"
                        % (sno, passwd))
                    res["message"] = "fault"
                    return res
                try:
                    models.StudentRank.objects.create(openid=openid, sno=sno,
                                                      avg_score=avg_score, department=login_student[0].department,
                                                      research=login_student[0].research,
                                                      rank_research=login_student[0].research)
                except Exception as e:
                    res["message"] = "fault"
                    logger.error(
                        "[student get rank white info repeated]: [sno]: %s [passwd]: %s [Exception]: %s"
                        % (sno, passwd, e))
            else:
                try:
                    # 如果登陆其它号了
                    if login_student[0].sno != rank_student[0].sno:
                        get_score = score.main(sno, passwd, "null")
                        if get_score["message"] == "success" and get_score["have_class"] == 1:
                            avg_score = get_score["mean"]
                        else:
                            logger.error(
                                "[student avg_score update fail]: [sno]: %s [passwd]: %s"
                                % (sno, passwd))
                            res["message"] = "fault"
                            return res
                        rank_student.update(sno=sno, avg_score=avg_score,
                                            rank_research=login_student[0].research,
                                            research=login_student[0].research,
                                            avg_score_update_date=timezone.now())
                        res["times"] = 1
                    # 如果没有登陆其他号
                    else:
                        if is_update_score:
                            get_score = score.main(sno, passwd, "null")
                            if get_score["message"] == "success" and get_score["have_class"] == 1:
                                avg_score = get_score["mean"]
                            else:
                                logger.error(
                                    "[student avg_score update fail]: [sno]: %s [passwd]: %s"
                                    % (sno, passwd))
                                res["message"] = "fault"
                                return res
                            rank_student.update(avg_score=avg_score,
                                                avg_score_update_date=timezone.now())
                            res["times"] = 2
                        else:
                            pass
                            res["times"] = 3
                except Exception as e:
                    res["message"] = "fault"
                    logger.error(
                        "[student rank white info repeated]: [sno]: %s [passwd]: %s [Exception]: %s"
                        % (sno, passwd, e))
        except Exception as e:
            res["message"] = "fault"
            logger.error(
                "[student rank white info repeated]: [sno]: %s [passwd]: %s [Exception]: %s"
                % (sno, passwd, e))
        return res

    @classmethod
    def interval_update_score(cls):
        try:
            config = models.Config.objects.all()[0]
            # 找出已经订阅的student
            for sno_start in range(int(config.score_rank_min), int(config.score_rank_max) + 1):
                students = models.Student.objects.filter(sno__startswith=str(sno_start))
                # 遍历列表
                travel_begin = time.time()
                for student in students:
                    try:
                        # 判断是否存在
                        cur_student = models.StudentRank.objects.filter(openid=student.openid)
                        # 不存在
                        if len(cur_student) == 0:
                            res = score.main(student.sno, cls.base64decode(student.passwd), "null")
                            if res["message"] == "success" and res["have_class"] == 1:
                                avg_score = res["mean"]
                            else:
                                logger.error(
                                    "[student avg_score update fail]: [sno]: %s [passwd]: %s"
                                    % (student.sno, student.passwd))
                                continue
                            try:
                                models.StudentRank.objects.create(openid=student.openid, sno=student.sno,
                                                                  avg_score=avg_score, department=student.department,
                                                                  research=student.research,
                                                                  rank_research=student.research)
                            except Exception as e:
                                logger.error(
                                    "[student rank white info repeated]: [sno]: %s [passwd]: %s [Exception]: %s"
                                    % (student.sno, student.passwd, e))
                        # 存在
                        else:
                            res = score.main(student.sno, cls.base64decode(student.passwd), "null")
                            if res["message"] == "success" and res["have_class"] == 1:
                                avg_score = res["mean"]
                            else:
                                logger.error(
                                    "[student avg_score update fail]: [sno]: %s [passwd]: %s"
                                    % (student.sno, student.passwd))
                                continue
                            try:
                                # 如果登陆其它号了
                                if student.sno != cur_student[0].sno:
                                    cur_student.update(sno=student.sno, avg_score=avg_score,
                                                       rank_research=student.research,
                                                       research=student.research,
                                                       travel_times=0,
                                                       avg_score_update_date=timezone.now())
                                # 如果没有登陆其他号
                                else:
                                    cur_student.update(avg_score=avg_score, avg_score_update_date=timezone.now())
                                    cur_student.travel_times += 1
                            except Exception as e:
                                logger.error(
                                    "[student rank white info repeated]: [sno]: %s [passwd]: %s [Exception]: %s"
                                    % (student.sno, student.passwd, e))
                        time.sleep(5)
                    except Exception as e:
                        logger.error("【成绩排名】遍历当前学生：%s失败! %s" % (student, e))
                travel_end = time.time()
                logger.info("【成绩排名】遍历%s个学生共耗时%ss" % (len(students), travel_end - travel_begin))
        except Exception as e:
            logger.error("【成绩排名】获取学生失败！ %s" % e)

    @classmethod
    def base64decode(cls, passwd):
        """数据库密码解密"""
        decode_passwd = base64.b64decode(passwd.encode('GBK')).decode('ascii')  # .decode('ascii') 转换成字符形式
        return decode_passwd

    @classmethod
    def __list_to_str(cls, arr):
        """
        将list转为以,分割的字符串，方便数据库存储
        :param arr:
        :return:
        """
        return ",".join(list(map(str, arr)))

    @classmethod
    def __str_to_list(cls, ele_type, string):
        """
        将数据库字符串转换成列表
        :param ele_type:
        :param string:
        :return:
        """
        if string == "" or string == "-":
            return []
        return list(map(ele_type, string.split(",")))
