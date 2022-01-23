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
                    Q(department=student[0].department) & Q(sno__startswith=sno_prefix)).values('research',
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
    def get_common_courses(cls, openid, sno):
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
    def check_allow_update_rank_score(cls):
        """
        判断系统是否允许更新成绩
        :return: Bool
        """
        config = models.Config.objects.first()
        if config is None:
            return True
        return config.is_open_rank_score_update == 1

    @classmethod
    def get_my_score_rank(cls, openid, sno, passwd, type):
        # 判断是否存在 openid sno passwd
        try:
            # 额外信息
            extra = {"is_open_rank_score_update": cls.check_allow_update_rank_score()}
            config = models.Config.objects.all()[0]
            sno_prefix = sno[:4]
            # 找出已经订阅的student
            if int(sno_prefix) in range(int(config.get_score_rank_nj_min), int(config.get_score_rank_nj_max) + 1):
                need_update = False if type == "0" else True
                res = cls.score_update(sno, passwd, openid, need_update)
                if res["message"] == "success":
                    # 查询当前访问的学生排名信息
                    student = models.StudentRank.objects.filter(openid=openid)
                    # 获取平均学分绩
                    avg_score = student[0].avg_score
                    # 研究方向
                    rank_research_list = cls.__str_to_list(str, student[0].rank_research)
                    # 专业和研究方向
                    processed_profession_list, processed_research_list = cls.__split_profession_and_research(rank_research_list)
                    all_student = models.StudentRank.objects.filter(Q(profession__in=processed_profession_list)
                                                                    & Q(research__in=processed_research_list)
                                                                    & Q(sno__startswith=sno_prefix)).values('sno').distinct().count()
                    # 如果没有不参与排名的课程
                    if student[0].exclude_courses == "-":
                        exclude_courses_list = []
                        not_in_exclude_course_avg_score = avg_score
                    else:
                        exclude_courses_list = cls.__str_to_list(str, student[0].exclude_courses)
                        not_in_exclude_course_avg_score = cls.__count_not_in_exclude_courses_avg_score(
                            exclude_courses_list, eval(student[0].courses_info))
                    # 获取成绩排名列表，按刷新时间降序
                    db_students_rank_info_list = models.StudentRank.objects.filter(Q(profession__in=processed_profession_list)
                                                                                   & Q(research__in=processed_research_list)
                                                                                   & Q(can_join_rank=1)
                                                                                   &Q(sno__startswith=sno_prefix)).order_by('-avg_score_update_date').all()
                    # get class duties
                    cur_student_login_info = models.Student.objects.filter(sno=sno, openid=openid).first()
                    has_class_duties = False
                    if cur_student_login_info is not None and cur_student_login_info.class_duties != 0:
                        has_class_duties = True
                    # 拼装排名
                    students_rank_info_list = []
                    sno_set = set()
                    for i in range(len(db_students_rank_info_list)):
                        cur_sno = db_students_rank_info_list[i].sno
                        if cur_sno not in sno_set:
                            sno_set.add(cur_sno)
                            # 计算平均学分绩
                            cur_avg_score = cls.__count_not_in_exclude_courses_avg_score(exclude_courses_list, eval(db_students_rank_info_list[i].courses_info))
                            cur_student_login_info_list = models.Student.objects.filter(sno=cur_sno)
                            full_name = cur_student_login_info_list[0].name if len(cur_student_login_info_list) >= 1 and (has_class_duties or cur_sno == sno) else "**"
                            if cur_sno != sno:
                                full_name = full_name + " | 最新更新:%s" % db_students_rank_info_list[i].avg_score_update_date.strftime("%Y-%m-%d %H:%M")
                            students_rank_info_list.append({
                                "sno": cur_sno,
                                "full_name": full_name,
                                "avg_score": cur_avg_score,
                                "profession_research": db_students_rank_info_list[i].profession + "(" + db_students_rank_info_list[i].research + ")"
                            })
                    # 成绩排序
                    sorted_students_rank_info_list = sorted(students_rank_info_list, key=lambda students_rank_info_list:students_rank_info_list['avg_score'], reverse=True)
                    # 不及格或者重修不参与排名
                    if str(student[0].can_join_rank) == "0":
                        return {"message": "success", "avg_score": avg_score,
                                "not_in_exclude_course_avg_score": "--",
                                "rank": "--", "rank_rate": 0, "add_same_rank": "--",
                                "add_same_rank_rate": 0, "same_student": "--",
                                "all_student": all_student, "research_list": rank_research_list,
                                "top_forty_percent_students": sorted_students_rank_info_list,
                                "exclude_courses": exclude_courses_list, "extra": extra}
                    same_student, flag, rank = 0, False, 0
                    for i in range(len(sorted_students_rank_info_list)):
                        if (sorted_students_rank_info_list[i]["sno"] == sno or sorted_students_rank_info_list[i]["avg_score"] == not_in_exclude_course_avg_score) and not flag:
                            rank = i + 1
                            flag = True
                        if sorted_students_rank_info_list[i]["avg_score"] == not_in_exclude_course_avg_score and sorted_students_rank_info_list[i]["sno"] != sno:
                            same_student += 1
                    rank_rate = round(rank / all_student, 4)
                    add_same_rank = rank + same_student
                    add_same_rank_rate = round(add_same_rank / all_student, 4)
                    return {"message": "success", "avg_score": avg_score,
                            "not_in_exclude_course_avg_score": not_in_exclude_course_avg_score,
                            "rank": rank, "rank_rate": rank_rate, "add_same_rank": add_same_rank,
                            "add_same_rank_rate": add_same_rank_rate, "same_student": same_student,
                            "all_student": all_student, "research_list": rank_research_list,
                            "top_forty_percent_students": sorted_students_rank_info_list,
                            "exclude_courses": exclude_courses_list, "extra": extra}
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
            # 如果当前登录的学生已经计算过平均学分绩
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
                        if is_update_score and cls.check_allow_update_rank_score():
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
            update_success_num = 0
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
                                update_success_num += 1
                                logger.info(
                                    "[%s成功添加至成绩排名]: [sno]: %s [passwd]: %s "
                                    % (student.sno, student.sno, student.passwd))
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
                                    "[get score fail]: [sno]: %s [passwd]: %s"
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
                                update_success_num += 1
                                logger.info("[%s参与成绩排名成绩更新成功]: [sno]: %s [passwd]: %s "
                                            % (student.sno, student.sno, student.passwd))
                            except Exception as e:
                                logger.error(
                                    "[student rank white info repeated]: [sno]: %s [passwd]: %s [Exception]: %s"
                                    % (student.sno, student.passwd, e))
                        time.sleep(2.0)
                    except Exception as e:
                        logger.error("【成绩排名】遍历当前学生：%s失败! %s" % (student, e))
                travel_end = time.time()
                logger.info("【成绩排名】遍历%s个学生共耗时%ss,%s个学生更新成绩成功，失败%s个学生"
                            % (len(students), travel_end - travel_begin,
                               update_success_num, len(students) - update_success_num))
        except Exception as e:
            logger.error("【成绩排名】遍历获取学生失败！ %s" % e)

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
