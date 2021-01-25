#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: qinchangshuai(cs_qin@qq.com) 
Date: 2021/1/22 13:35 
"""
import time
import base64
import django.utils.timezone as timezone
from django.db.models import Q

from OUC import models
from OUC.core import score
from OUC import log

logger = log.logger


class ScoreRank(object):

    @classmethod
    def get_department_all_research(cls, openid, sno):
        try:
            config = models.Config.objects.all()[0]
            sno_prefix = sno[:4]
            # 找出已经订阅的student
            if int(sno_prefix) in range(int(config.get_score_rank_nj_min), int(config.get_score_rank_nj_max) + 1):
                student = models.StudentRank.objects.filter(openid=openid)
                # 同年级 同选择研究方向的人数
                research_list = cls.__str_to_list(str, student[0].rank_research)
                unique_research = student[0].research
                query_research_list = models.StudentRank.objects.filter(Q(sno__startswith=sno_prefix) & Q(department=student[0].department)).values('research', 'profession').distinct()
                all_research_list = [{"name": (cur_student["profession"] + "(" + cur_student["research"] + ")"), "value": cur_student["research"]} for cur_student in query_research_list]
                for research in all_research_list:
                    if research["value"] in research_list:
                        research["checked"] = True
                    else:
                        research["checked"] = False

                    if research["value"] == unique_research:
                        research["disabled"] = True
                    else:
                        research["disabled"] = False
                all_research_list = sorted(all_research_list, key=lambda keys: keys['name'])
                return {"message": "success", "all_research_list": all_research_list}
            else:
                return {"message": "illegal"}
        except Exception as e:
            logger.error(
                "[get my department profession]: [sno]: %s [passwd]: %s [Exception]: %s"
                % (sno, passwd, e))
            return {"message": "fault"}

    @classmethod
    def set_join_rank_research(cls, openid, research_list):
        try:
            rank_student = models.StudentRank.objects.filter(openid=openid)
            rank_student.update(rank_research=research_list)
            return {"message": "success"}
        except Exception as e:
            logger.error(
                "[get my department profession]: [sno]: %s [passwd]: %s [Exception]: %s"
                % (sno, passwd, e))
            return {"message": "fault"}

    @classmethod
    def get_my_score_rank(cls, openid, sno, passwd, type):
        # 判断是否存在 openid sno passwd
        try:
            config = models.Config.objects.all()[0]
            sno_prefix = sno[:4]
            # 找出已经订阅的student
            if int(sno_prefix) in range(int(config.get_score_rank_nj_min), int(config.get_score_rank_nj_max) + 1):
                need_update = False if type == "0" else True
                res = cls.score_update(sno, passwd, openid, need_update)
                if res["message"] == "success":
                    student = models.StudentRank.objects.filter(openid=openid)
                    avg_score = student[0].avg_score
                    research_list = cls.__str_to_list(str, student[0].rank_research)
                    # 同年级 同选择研究方向的人数
                    all_people = models.StudentRank.objects.filter(Q(sno__startswith=sno_prefix) & Q(research__in=research_list)).count()
                    # 同年级 选择研究方向范围内比自己分高的人数
                    rank_list = models.StudentRank.objects.filter(Q(sno__startswith=sno_prefix) & Q(research__in=research_list) & Q(avg_score__gte=student[0].avg_score)).exclude(openid=openid)
                    # print(rank_list)
                    # 相同分数的人数
                    same_people_list = models.StudentRank.objects.filter(Q(sno__startswith=sno_prefix) & Q(research__in=research_list) & Q(avg_score=student[0].avg_score)).exclude(openid=openid)
                    same_people = len(same_people_list)
                    rank = len(rank_list) + 1
                    rank_rate = round(rank / all_people, 4)
                    add_same_rank = rank + same_people
                    add_same_rank_rate = round(add_same_rank / all_people, 4)
                    return {"message": "success", "avg_score": avg_score, "rank": rank, "rank_rate": rank_rate,
                            "add_same_rank": add_same_rank, "add_same_rank_rate": add_same_rank_rate,
                            "same_people": same_people, "all_people": all_people,
                            "research_string": student[0].rank_research, "research_list": research_list}
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
            # 如果当前登录的学生没有计算平均学分绩
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
                                                      profession=login_student[0].profession,
                                                      research=login_student[0].research,
                                                      rank_research=login_student[0].research)
                except Exception as e:
                    res["message"] = "fault"
                    logger.error(
                        "[student get rank white info repeated]: [sno]: %s [passwd]: %s [Exception]: %s"
                        % (sno, passwd, e))
            # 如果当前登录的学生计算平均学分绩
            else:
                try:
                    # 如果当前学生又登陆其它号了
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
                                            department=login_student[0].department,
                                            profession=login_student[0].profession,
                                            research=login_student[0].research,
                                            rank_research=login_student[0].research,
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
            for sno_start in range(int(config.score_rank_travel_nj_min), int(config.score_rank_travel_nj_max) + 1):
                # 找出符合学号年级的所有学生
                students = models.Student.objects.filter(sno__startswith=str(sno_start))
                # 遍历列表开始时间
                travel_begin = time.time()
                for student in students:
                    try:
                        # 判断是否存在当前成绩排名的列表当中
                        cur_student = models.StudentRank.objects.filter(openid=student.openid)
                        # 如果当前登录的学生没有计算平均学分绩
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
                                                                  profession=student.profession,
                                                                  research=student.research,
                                                                  rank_research=student.research)
                            except Exception as e:
                                logger.error(
                                    "[student rank white info repeated]: [sno]: %s [passwd]: %s [Exception]: %s"
                                    % (student.sno, student.passwd, e))
                        # 如果当前登录的学生已经计算平均学分绩
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
                                                       department=student.department,
                                                       profession=student.profession,
                                                       research=student.research,
                                                       rank_research=student.research,
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
                        time.sleep(3)
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
