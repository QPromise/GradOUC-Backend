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
                unique_profession = student[0].profession
                query_research_list = models.StudentRank.objects.filter(
                    Q(sno__startswith=sno_prefix) & Q(department=student[0].department)).values('research',
                                                                                                'profession').distinct()
                all_research_list = [{"name": (cur_student["profession"] + "(" + cur_student["research"] + ")"),
                                      "value": cur_student["profession"] + "&&" + cur_student["research"]} for
                                     cur_student in query_research_list]
                for research in all_research_list:
                    if research["value"] in research_list:
                        research["checked"] = True
                    else:
                        research["checked"] = False

                    if research["value"] == unique_profession + "&&" + unique_research:
                        research["disabled"] = True
                    else:
                        research["disabled"] = False
                all_research_list = sorted(all_research_list, key=lambda keys: keys['name'])
                return {"message": "success", "all_research_list": all_research_list}
            else:
                return {"message": "illegal"}
        except Exception as e:
            logger.error(
                "[get my department profession]: [sno]: %s [Exception]: %s"
                % (sno, e))
            return {"message": "fault"}

    @classmethod
    def set_join_rank_research(cls, openid, research_list):
        try:
            rank_student = models.StudentRank.objects.filter(openid=openid)
            if research_list != rank_student[0].rank_research:
                rank_student.update(rank_research=research_list)
                # rank_student.update(exclude_courses="-")
            return {"message": "success"}
        except Exception as e:
            logger.error(
                "[set join rank research]: [openid]: %s [research list]: %s [Exception]: %s"
                % (openid, research_list, e))
            return {"message": "fault"}

    @classmethod
    def get_commom_courses(cls, openid, sno):
        try:
            config = models.Config.objects.all()[0]
            sno_prefix = sno[:4]
            # 找出已经订阅的student
            if int(sno_prefix) in range(int(config.get_score_rank_nj_min), int(config.get_score_rank_nj_max) + 1):
                student = models.StudentRank.objects.filter(openid=openid)
                exclude_courses_list = cls.__str_to_list(str, student[0].exclude_courses)
                common_courses_name_list = cls.__str_to_list(str, student[0].courses_name)
                common_courses_type_list = cls.__str_to_list(str, student[0].courses_type)
                common_courses = []
                for course in common_courses_name_list:
                    cur_course = dict()
                    cur_course["value"] = course
                    cur_course["type"] = "name"
                    if course in exclude_courses_list:
                        cur_course["checked"] = True
                    else:
                        cur_course["checked"] = False
                    common_courses.append(cur_course)
                common_courses_type = []
                for course_type in common_courses_type_list:
                    cur_course = dict()
                    cur_course["value"] = course_type
                    cur_course["type"] = "type"
                    if course_type in exclude_courses_list:
                        cur_course["checked"] = True
                    else:
                        cur_course["checked"] = False
                    common_courses_type.append(cur_course)
                return {"message": "success", "common_courses": common_courses, "common_courses_type": common_courses_type}
            else:
                return {"message": "illegal"}
        except Exception as e:
            logger.error("[get common courses]: [sno]: %s [Exception]: %s" % (sno, e))
            return {"message": "fault"}

    @classmethod
    def set_exclude_courses(cls, openid, select_common_courses):
        try:
            rank_student = models.StudentRank.objects.filter(openid=openid)
            if select_common_courses == "":
                rank_student.update(exclude_courses="-")
            else:
                rank_student.update(exclude_courses=select_common_courses)
            return {"message": "success"}
        except Exception as e:
            logger.error("[set exclude courses]: [openid]: %s [Exception]: %s" % (openid, e))
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
                    rank_research_list = cls.__str_to_list(str, student[0].rank_research)
                    processed_profession_list, processed_research_list = cls.__split_profession_and_research(
                        rank_research_list)
                    all_student = models.StudentRank.objects.filter(
                        Q(sno__startswith=sno_prefix)
                        & Q(profession__in=processed_profession_list)
                        & Q(research__in=processed_research_list)).values('sno').distinct().count()
                    # 如果没设置不参评的科目
                    if student[0].exclude_courses == "-":
                        # 同年级 同选择研究方向的人数
                        top_forty_student_list = models.StudentRank.objects.filter(
                            Q(sno__startswith=sno_prefix)
                            & Q(profession__in=processed_profession_list)
                            & Q(research__in=processed_research_list)
                            & Q(can_join_rank=1)).order_by('-avg_score').values('sno',
                                                                                'avg_score',
                                                                                'profession',
                                                                                'research').distinct().all()
                        top_forty_percent_students = []
                        for i in range(len(top_forty_student_list)):
                            stu = models.Student.objects.filter(sno=top_forty_student_list[i]["sno"])
                            stu_name = stu[0].name if len(stu) >= 1 else "**"
                            stu_sno = top_forty_student_list[i]["sno"]
                            if stu_sno == sno:
                                full_name = stu_name
                            else:
                                full_name = "**"
                            top_forty_percent_students.append(
                                {"sno": stu_sno, "full_name": full_name, "avg_score": top_forty_student_list[i]["avg_score"],
                                 "profession_research": top_forty_student_list[i]["profession"] + "(" + top_forty_student_list[i][
                                     "research"] + ")"})
                        # 不及格或者重修不参与排名
                        if str(student[0].can_join_rank) == "0":
                            return {"message": "success", "avg_score": avg_score,
                                    "not_in_exclude_course_avg_score": "--",
                                    "rank": "--", "rank_rate": 0, "add_same_rank": "--",
                                    "add_same_rank_rate": 0, "same_student": "--",
                                    "all_student": all_student, "research_list": rank_research_list,
                                    "top_forty_percent_students": top_forty_percent_students,
                                    "exclude_courses": []}
                        # 同年级 选择研究方向范围内比自己分高的人数
                        rank_list_len = models.StudentRank.objects.filter(
                            Q(sno__startswith=sno_prefix) & Q(profession__in=processed_profession_list)
                            & Q(research__in=processed_research_list) & Q(avg_score__gt=student[0].avg_score)
                            & Q(can_join_rank=1)).exclude(openid=openid).exclude(sno=sno).values('sno').distinct().count()
                        # 相同分数的人数
                        same_student_list_len = models.StudentRank.objects.filter(
                            Q(sno__startswith=sno_prefix) & Q(profession__in=processed_profession_list)
                            & Q(research__in=processed_research_list) & Q(avg_score=student[0].avg_score)
                            & Q(can_join_rank=1)).exclude(openid=openid).exclude(sno=sno).values('sno').distinct().count()
                        same_student = same_student_list_len
                        rank = rank_list_len + 1
                        rank_rate = round(rank / all_student, 4)
                        add_same_rank = rank + same_student
                        add_same_rank_rate = round(add_same_rank / all_student, 4)
                        return {"message": "success", "avg_score": avg_score, "not_in_exclude_course_avg_score": avg_score,
                                "rank": rank, "rank_rate": rank_rate, "add_same_rank": add_same_rank,
                                "add_same_rank_rate": add_same_rank_rate, "same_student": same_student,
                                "all_student": all_student, "research_list": rank_research_list,
                                "top_forty_percent_students": top_forty_percent_students,
                                "exclude_courses": []}
                    # 如果设置了不参评的科目
                    else:
                        exclude_courses_list = cls.__str_to_list(str, student[0].exclude_courses)
                        not_in_exclude_course_avg_score = cls.__count_not_in_exclude_courses_avg_score(exclude_courses_list, eval(student[0].courses_info))
                        in_research_students = models.StudentRank.objects.filter(Q(sno__startswith=sno_prefix)
                                                                                 & Q(profession__in=processed_profession_list)
                                                                                 & Q(research__in=processed_research_list)
                                                                                 & Q(can_join_rank=1)).all()
                        in_research_students_info = []
                        sno_set = set()
                        for i in range(len(in_research_students)):
                            cur_sno = in_research_students[i].sno
                            if cur_sno not in sno_set:
                                sno_set.add(cur_sno)
                                # 计算平均学分绩
                                cur_avg_score = cls.__count_not_in_exclude_courses_avg_score(exclude_courses_list, eval(in_research_students[i].courses_info))
                                stu = models.Student.objects.filter(sno=cur_sno)
                                stu_name = stu[0].name if len(stu) >= 1 else "**"
                                if cur_sno == sno:
                                    full_name = stu_name
                                else:
                                    full_name = "**"
                                in_research_students_info.append({
                                    "sno": cur_sno,
                                    "full_name": full_name,
                                    "avg_score": cur_avg_score,
                                    "profession_research": in_research_students[i].profession + "(" + in_research_students[i].research + ")"
                                })
                        sorted_in_research_students_info = sorted(in_research_students_info, key=lambda in_research_students_info: in_research_students_info['avg_score'], reverse=True)
                        top_forty_percent_students = sorted_in_research_students_info
                        # 不及格或者重修不参与排名
                        if str(student[0].can_join_rank) == "0":
                            return {"message": "success", "avg_score": avg_score,
                                    "not_in_exclude_course_avg_score": "--",
                                    "rank": "--", "rank_rate": 0, "add_same_rank": "--",
                                    "add_same_rank_rate": 0, "same_student": "--",
                                    "all_student": all_student, "research_list": rank_research_list,
                                    "top_forty_percent_students": top_forty_percent_students,
                                    "exclude_courses": exclude_courses_list}
                        same_student = 0
                        flag = 0
                        for i in range(len(sorted_in_research_students_info)):
                            if (sorted_in_research_students_info[i]["sno"] == sno or sorted_in_research_students_info[i]["avg_score"] == not_in_exclude_course_avg_score) and not flag:
                                rank = i + 1
                                flag = 1
                            if sorted_in_research_students_info[i]["avg_score"] == not_in_exclude_course_avg_score and sorted_in_research_students_info[i]["sno"] != sno:
                                same_student += 1
                        rank_rate = round(rank / all_student, 4)
                        add_same_rank = rank + same_student
                        add_same_rank_rate = round(add_same_rank / all_student, 4)
                        return {"message": "success", "avg_score": avg_score,
                                "not_in_exclude_course_avg_score": not_in_exclude_course_avg_score,
                                "rank": rank, "rank_rate": rank_rate, "add_same_rank": add_same_rank,
                                "add_same_rank_rate": add_same_rank_rate, "same_student": same_student,
                                "all_student": all_student, "research_list": rank_research_list,
                                "top_forty_percent_students": top_forty_percent_students,
                                "exclude_courses": exclude_courses_list}
                else:
                    return {"message": res["message"]}
            else:
                return {"message": "illegal"}
        except Exception as e:
            logger.error(
                "[get my rank fail]: [sno]: %s [passwd]: %s [Exception]: %s"
                % (sno, passwd, e))
            return {"message": "fault"}

    @classmethod
    def __count_not_in_exclude_courses_avg_score(cls, exclude_courses, courses):
        total_credit = 0.0
        total_score = 0.0
        avg_score = 0.0
        for i in range(len(courses)):
            if courses[i]["name"] not in exclude_courses and courses[i]["type"] not in exclude_courses:
                if courses[i]["selected"] and courses[i]["credit"]:
                    total_credit += float(courses[i]["credit"])
                    total_score += float(courses[i]["score"]) * float(courses[i]["credit"])
        if total_credit != 0:
            avg_score = round(total_score / total_credit, 4)
        return avg_score

    @classmethod
    def score_update(cls, sno, passwd, openid, is_update_score):
        res = {"message": "success", "times": 0}
        try:
            rank_student = models.StudentRank.objects.filter(openid=openid)
            login_student = models.Student.objects.filter(openid=openid)
            # 如果当前登录的学生没有计算平均学分绩
            if len(rank_student) == 0:
                # 如果之前登录信息没有存储数据库
                if len(login_student) == 0:
                    get_score = score.main(sno, passwd, openid)
                    login_student = models.Student.objects.filter(openid=openid)
                else:
                    get_score = score.main(sno, passwd, "null")
                if get_score["message"] == "success" and get_score["have_class"] == 1:
                    avg_score = get_score["mean"]
                    courses = get_score["courses"]
                    can_join_rank = get_score["can_join_rank"]
                    courses_name = []
                    courses_type = set()
                    # 添加可以计算平均学分绩的课程
                    for i in range(len(courses)):
                        if courses[i]["selected"]:
                            courses_name.append(courses[i]["name"])
                        courses_type.add(courses[i]["type"])
                    courses_type = list(courses_type)
                else:
                    logger.error(
                        "[student avg_score update fail]: [sno]: %s [passwd]: %s"
                        % (sno, passwd))
                    res["message"] = get_score["message"]
                    return res
                try:
                    models.StudentRank.objects.create(openid=openid, sno=sno,
                                                      avg_score=avg_score, department=login_student[0].department,
                                                      profession=login_student[0].profession,
                                                      research=login_student[0].research,
                                                      rank_research=login_student[0].profession + "&&" + login_student[0].research,
                                                      courses_info=courses,
                                                      can_join_rank=can_join_rank,
                                                      courses_name=cls.__list_to_str(courses_name),
                                                      courses_type=cls.__list_to_str(courses_type)
                                                      )
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
                            courses = get_score["courses"]
                            can_join_rank = get_score["can_join_rank"]
                            courses_name = []
                            courses_type = set()
                            # 添加可以计算平均学分绩的课程
                            for i in range(len(courses)):
                                if courses[i]["selected"]:
                                    courses_name.append(courses[i]["name"])
                                courses_type.add(courses[i]["type"])
                            courses_type = list(courses_type)
                        else:
                            logger.error(
                                "[student avg_score update fail]: [sno]: %s [passwd]: %s"
                                % (sno, passwd))
                            res["message"] = get_score["message"]
                            return res
                        rank_student.update(sno=sno, avg_score=avg_score,
                                            department=login_student[0].department,
                                            profession=login_student[0].profession,
                                            research=login_student[0].research,
                                            rank_research=login_student[0].profession + "&&" + login_student[0].research,
                                            courses_info=courses,
                                            exclude_courses="-",
                                            can_join_rank=can_join_rank,
                                            courses_name=cls.__list_to_str(courses_name),
                                            courses_type=cls.__list_to_str(courses_type),
                                            avg_score_update_date=timezone.now())
                        res["times"] = 1
                    # 如果没有登陆其他号
                    else:
                        if is_update_score:
                            get_score = score.main(sno, passwd, "null")
                            if get_score["message"] == "success" and get_score["have_class"] == 1:
                                avg_score = get_score["mean"]
                                courses = get_score["courses"]
                                can_join_rank = get_score["can_join_rank"]
                                courses_name = []
                                courses_type = set()
                                # 添加可以计算平均学分绩的课程
                                for i in range(len(courses)):
                                    if courses[i]["selected"]:
                                        courses_name.append(courses[i]["name"])
                                    courses_type.add(courses[i]["type"])
                                courses_type = list(courses_type)
                            else:
                                logger.error(
                                    "[student avg_score update fail]: [sno]: %s [passwd]: %s"
                                    % (sno, passwd))
                                res["message"] = get_score["message"]
                                return res
                            rank_student.update(avg_score=avg_score,
                                                courses_info=courses,
                                                can_join_rank=can_join_rank,
                                                courses_name=cls.__list_to_str(courses_name),
                                                courses_type=cls.__list_to_str(courses_type),
                                                avg_score_update_date=timezone.now())
                            res["times"] = 2
                        else:
                            res["times"] = 3
                except Exception as e:
                    res["message"] = "fault"
                    logger.error(
                        "[当前登录的学生已经计算平均学分绩]: [sno]: %s [passwd]: %s [Exception]: %s"
                        % (sno, passwd, e))
        except Exception as e:
            res["message"] = "fault"
            logger.error(
                "[当前登录的学生没有计算平均学分绩]: [sno]: %s [passwd]: %s [Exception]: %s"
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
                            get_score = score.main(student.sno, cls.base64decode(student.passwd), "null")
                            if get_score["message"] == "success" and get_score["have_class"] == 1:
                                avg_score = get_score["mean"]
                                courses = get_score["courses"]
                                can_join_rank = get_score["can_join_rank"]
                                courses_name = []
                                courses_type = set()
                                # 添加可以计算平均学分绩的课程
                                for i in range(len(courses)):
                                    if courses[i]["selected"]:
                                        courses_name.append(courses[i]["name"])
                                    courses_type.add(courses[i]["type"])
                                courses_type = list(courses_type)
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
                                                                  rank_research=student.profession + "&&" + student.research,
                                                                  courses_info=courses,
                                                                  can_join_rank=can_join_rank,
                                                                  courses_name=cls.__list_to_str(courses_name),
                                                                  courses_type=cls.__list_to_str(courses_type)
                                                                  )
                            except Exception as e:
                                logger.error(
                                    "[student rank white info repeated]: [sno]: %s [passwd]: %s [Exception]: %s"
                                    % (student.sno, student.passwd, e))
                        # 如果当前登录的学生已经计算平均学分绩
                        else:
                            get_score = score.main(student.sno, cls.base64decode(student.passwd), "null")
                            if get_score["message"] == "success" and get_score["have_class"] == 1:
                                avg_score = get_score["mean"]
                                courses = get_score["courses"]
                                can_join_rank = get_score["can_join_rank"]
                                courses_name = []
                                courses_type = set()
                                # 添加可以计算平均学分绩的课程
                                for i in range(len(courses)):
                                    if courses[i]["selected"]:
                                        courses_name.append(courses[i]["name"])
                                    courses_type.add(courses[i]["type"])
                                courses_type = list(courses_type)
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
                                                       rank_research=student.profession + "&&" + student.research,
                                                       travel_nums=0,
                                                       exclude_courses="-",
                                                       can_join_rank=can_join_rank,
                                                       avg_score_update_date=timezone.now(),
                                                       courses_info=courses,
                                                       courses_name=cls.__list_to_str(courses_name),
                                                       courses_type=cls.__list_to_str(courses_type)
                                                       )
                                # 如果没有登陆其他号
                                else:
                                    cur_student.update(avg_score=avg_score,
                                                       courses_info=courses,
                                                       can_join_rank=can_join_rank,
                                                       courses_name=cls.__list_to_str(courses_name),
                                                       courses_type=cls.__list_to_str(courses_type),
                                                       travel_nums=cur_student[0].travel_nums + 1,
                                                       avg_score_update_date=timezone.now())
                            except Exception as e:
                                logger.error(
                                    "[student rank white info repeated]: [sno]: %s [passwd]: %s [Exception]: %s"
                                    % (student.sno, student.passwd, e))
                        time.sleep(2.0)
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
        if len(arr) == 0:
            return "-"
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

    @classmethod
    def __split_profession_and_research(cls, rank_research_list):
        processed_rank_profession = []
        processed_rank_research = []
        for rank_research in rank_research_list:
            pair = rank_research.split("&&")
            processed_rank_profession.append(pair[0])
            processed_rank_research.append(pair[1])
        return processed_rank_profession, processed_rank_research
