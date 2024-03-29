#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: qinchangshuai(cs_qin@qq.com) 
Date: 2020/12/20 12:03 
"""
import requests
import json
import time
import threading
import base64
import re

from OUC import models
from OUC.core import score
from OUC import log

logger = log.logger


class AccessToken(object):
    _instance_lock = threading.Lock()

    access_token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" \
                       % ("wx2217b0fce3891980", "674cf5c56dfea43dca6c9236835d9376")
    access_token = None

    def __init__(self):
        pass

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(AccessToken, "_instance"):
            with AccessToken._instance_lock:
                if not hasattr(AccessToken, "_instance"):
                    AccessToken._instance = object.__new__(cls)
        return AccessToken._instance

    @classmethod
    def update_access_token(cls):
        try:
            get_result = requests.get(cls.access_token_url, timeout=6)
            get_result_json = get_result.json()
            access_token = get_result_json["access_token"]
            cls.access_token = access_token
            # print(AccessToken.access_token)
        except Exception as e:
            logger.error("获取token异常%s" % e)
            cls.access_token = None


class SubscribeScore(object):
    """

    """
    send_url_prefix = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token="
    template_id = "LxOu_CBTn3H88ndcz_S9aeRO_lTaR3lgKrIU2VoOuZo"

    @classmethod
    def set_failure_popup_false(cls, openid):
        if openid == "null":
            return {"message": False}
        try:
            subscribe_student = models.SubscribeStudent.objects.filter(openid=openid)
            if len(subscribe_student) == 0:
                return {"message": False}
            else:
                subscribe_student[0].failure_popup = 0
                subscribe_student[0].save()
                return {"message": True}
        except Exception as e:
            logger.error("用户openid=%s关闭成绩通知失效提示失败！%s" % (openid, e))
            return {"message": False}

    @classmethod
    def get_subscribe_status(cls, openid):
        """
        查看是否订阅
        :param openid:
        :return:
        """
        if openid == "null":
            return {"score_notice": False, "open_failure_popup": False, "times": 0}
        try:
            subscribe_student = models.SubscribeStudent.objects.filter(openid=openid)
            if len(subscribe_student) == 0:
                return {"score_notice": False, "open_failure_popup": False, "times": 0}
            else:
                times = subscribe_student[0].status
                if subscribe_student[0].legal_subscribe_date != "-":
                    legal_subscribe_dates = cls.__str_to_list(int, subscribe_student[0].legal_subscribe_date)
                    new_legal_subscribe_dates = []
                    for timestamp in legal_subscribe_dates:
                        print(int(time.time()), timestamp, type(timestamp))
                        if (int(time.time()) - timestamp) // (3600 * 24) < 7:
                            new_legal_subscribe_dates.append(timestamp)
                    times = len(new_legal_subscribe_dates)
                    subscribe_student[0].status = times
                    if len(new_legal_subscribe_dates) == 0:
                        subscribe_student[0].legal_subscribe_date = "-"
                    else:
                        subscribe_student[0].legal_subscribe_date = cls.__list_to_str(new_legal_subscribe_dates)
                    subscribe_student[0].save()
                score_notice = False if times == 0 else True
                if subscribe_student[0].failure_popup == 1:
                    return {"score_notice": score_notice, "open_failure_popup": True, "times": times}
                else:
                    return {"score_notice": score_notice, "open_failure_popup": False, "times": times}
        except Exception as e:
            logger.error("用户openid=%s获取自己的订阅状态失败！%s" % (openid, e))
            return {"score_notice": False, "open_failure_popup": False, "times": 0}

    @classmethod
    def subscribe_score(cls, openid):
        """
        用户进行订阅
        :param openid:
        :return:
        """
        if openid == "null":
            return {"message": "fault"}
        res = {"message": ""}
        try:
            student = models.Student.objects.filter(openid=openid)
            if len(student) != 0:
                subscribe_student = models.SubscribeStudent.objects.filter(openid=openid)
                if len(subscribe_student) == 0:
                    try:
                        models.SubscribeStudent.objects.create(openid=openid, sno=student[0].sno, status=1, legal_subscribe_date=int(time.time()))
                        res["message"] = "success"
                    except Exception as e:
                        res["message"] = "repeated"
                        logger.error("[write subscribe student info repeated]: [openid]: %s [Exception]: %s"
                                     % (openid, e))
                else:
                    if subscribe_student[0].status == 0:
                        subscribe_student[0].status = 1
                        subscribe_student[0].legal_subscribe_date = int(time.time())
                        subscribe_student[0].save()
                        res["message"] = "success"
                    else:
                        # 将数据库中的已有数据给修改一下
                        if subscribe_student[0].legal_subscribe_date == "-":
                            subscribe_student[0].status = 1
                            subscribe_student[0].legal_subscribe_date = int(time.time())
                            subscribe_student[0].save()
                        else:
                            # 多点一个订阅就把当前的时间给加进去，次数同时加一
                            subscribe_student[0].status = subscribe_student[0].status + 1
                            legal_subscribe_dates = cls.__str_to_list(int, subscribe_student[0].legal_subscribe_date)
                            legal_subscribe_dates.append(int(time.time()))
                            subscribe_student[0].legal_subscribe_date = cls.__list_to_str(legal_subscribe_dates)
                            subscribe_student[0].save()
                        res["message"] = "repeated"
            else:
                res["message"] = "fault"
            return res
        except Exception as e:
            logger.error("用户openid=%s订阅失败！%s" % (openid, e))
            return {"message": "fault"}

    @classmethod
    def send_score(cls, openid, name, sno, course_num, course_name, course_score):
        """
        出成绩了发送成绩，返回状态码，如果是43101代表用户取消订阅
        :param openid:
        :param name:
        :param sno:
        :param course_num:
        :param course_name:
        :param course_score:
        :return:
        """
        try:
            if AccessToken.access_token is not None:
                if len(course_name) > 19:
                    course_name = course_name[:15] + "..."
                send_url = cls.send_url_prefix + AccessToken.access_token
                values = {
                    "touser": openid,
                    "template_id": cls.template_id,
                    "page": "pages/core/score/score",
                    "lang": "zh_CN",
                    "data": {
                        "name1": {
                            "value": name
                        },
                        "number2": {
                            "value": sno
                        },
                        "number3": {
                            "value": course_num
                        },
                        "thing4": {
                            "value": course_name
                        },
                        "number5": {
                            "value": course_score
                        }
                    }
                }
                response = requests.post(send_url, json=values, timeout=6)
                resp_to_json = response.json()
                # print(resp_to_json)
                if resp_to_json["errcode"] != 0:
                    logger.error("[sno]: %s [name]: %s [errcode]: %s [errmsg]: %s"
                                 % (sno, name, resp_to_json["errcode"], resp_to_json["errmsg"]))
                    # print("error", resp_to_json["errcode"], resp_to_json["errmsg"])
                return resp_to_json["errcode"]
            else:
                logger.error("[sno]: %s [name]: %s [get token error]: %s" % (sno, name, "获取token失败"))
                return 500
        except Exception as e:
            logger.error("[sno]: %s [name]: %s [Exception]: %s" % (sno, name, e))
            return 500

    @classmethod
    def score_compare(cls, openid, sno, passwd, name, db_get_scores, subscribe_student):
        """
        如果成绩跟之前数据库存储的对比有变化，则调用send_score方法
        :param openid:
        :param sno:
        :param passwd:
        :param name:
        :param db_get_scores:
        :return:
        """
        res = score.main(sno, passwd, "null")
        if res["message"] == "success" and res["have_class"] == 1:
            courses = res["courses"]
            # 如果用户是第一次或者切换过账号
            if db_get_scores == "-":
                try:
                    db_write_scores = [course["score"] for course in courses]
                    db_write_scores_str = cls.__list_to_str(db_write_scores)
                    subscribe_student.sno = sno
                    subscribe_student.scores = db_write_scores_str
                    subscribe_student.save()
                except Exception as e:
                    logger.error("[sno]: %s [passwd]: %s [第一次保存课表失败]: [Exception]: %s" % (sno, passwd, e))
                # models.SubscribeStudent.objects.filter(openid=openid).update(sno=sno, scores=db_write_scores_str)
            # 其它
            else:
                db_write_scores = cls.__str_to_list(str, db_get_scores)
                if len(courses) == len(db_write_scores):
                    try:
                        for i in range(len(courses)):
                            cur_score = courses[i]["score"]
                            # 之前数据库存储的是已经出的数字
                            if re.search(r"(\d+)", db_write_scores[i]):
                                tmp_db_write_score = float(db_write_scores[i])
                            else:
                                tmp_db_write_score = db_write_scores[i]
                            # 如果与数据库存储的成绩不一样
                            if cur_score != tmp_db_write_score:
                                # 如果课表发生了变动，出现选课的情况，直接把最新的写入
                                if cur_score == "未出" or cur_score == "未选" or tmp_db_write_score == "未选":
                                    db_write_scores = [course["score"] for course in courses]
                                    db_write_scores_str = cls.__list_to_str(db_write_scores)
                                    subscribe_student.sno = sno
                                    subscribe_student.scores = db_write_scores_str
                                    subscribe_student.save()
                                    break
                                # 这是成绩更新的情况，先写入数据库，然后直接发消息，退出
                                res_code = cls.send_score(openid, name, sno, "1001", courses[i]["name"], cur_score)
                                if res_code == 0:
                                    subscribe_student.new_send_message = "%s:%s -> %s" % (
                                        courses[i]["name"], db_write_scores[i], cur_score)
                                    db_write_scores[i] = cur_score
                                    db_write_scores_str = cls.__list_to_str(db_write_scores)

                                    if subscribe_student.status - 1 <= 0:
                                        subscribe_student.status = 0
                                        subscribe_student.legal_subscribe_date = "-"
                                    else:
                                        subscribe_student.status = subscribe_student.status - 1
                                        if subscribe_student.legal_subscribe_date == "-":
                                            pass
                                        else:
                                            legal_subscribe_dates = cls.__str_to_list(int, subscribe_student.legal_subscribe_date)
                                            if len(legal_subscribe_dates) == 1:
                                                subscribe_student.legal_subscribe_date = "-"
                                            else:
                                                subscribe_student.legal_subscribe_date = cls.__list_to_str(legal_subscribe_dates[1:])

                                    subscribe_student.scores = db_write_scores_str
                                    subscribe_student.send_success_nums = subscribe_student.send_success_nums + 1
                                    subscribe_student.save()
                                elif res_code == 43101:
                                    # 当用户取消订阅的时候
                                    subscribe_student.status = 0
                                    subscribe_student.legal_subscribe_date = "-"
                                    subscribe_student.send_fail_nums = subscribe_student.send_fail_nums + 1
                                    subscribe_student.save()
                                    # models.SubscribeStudent.objects.filter(
                                    #     openid=openid).update(status=0)
                                else:
                                    subscribe_student.send_fail_nums = subscribe_student.send_fail_nums + 1
                                    subscribe_student.save()
                                    # models.SubscribeStudent.objects.filter(
                                    #     openid=openid).update(scores=db_write_scores_str)
                                break
                    except Exception as e:
                        logger.error("[sno]: %s [passwd]: %s [比较数据库与新抓取的课表出现异常]: [Exception]: %s" % (sno, passwd, e))
                else:
                    try:
                        db_write_scores = [course["score"] for course in courses]
                        db_write_scores_str = cls.__list_to_str(db_write_scores)
                        subscribe_student.sno = sno
                        subscribe_student.scores = db_write_scores_str
                        subscribe_student.save()
                    except Exception as e:
                        logger.error("[sno]: %s [passwd]: %s [与之前课表长度不一样，保存新课表异常]: [Exception]: %s" % (sno, passwd, e))
        else:
            logger.error("[sno]: %s [name]: %s [获取课表失败]: [reason]: %s" % (sno, name, res))

    @classmethod
    def travel_subscribe_students(cls):
        """
        遍历已经订阅的数据库表，去查找学号密码，如果成绩有变动则通知，时间间隔十五分钟（多线程改进）
        :return:
        """
        try:
            # 找出已经订阅的student
            subscribe_students = models.SubscribeStudent.objects.filter(status__gte=1)
            # 遍历列表
            travel_begin = time.time()
            for subscribe_student in subscribe_students:
                try:
                    # 判断是否重新进行了登录
                    cur_student = models.Student.objects.filter(openid=subscribe_student.openid)[0]
                    if cur_student.sno != subscribe_student.sno:
                        db_scores = "-"
                    else:
                        db_scores = subscribe_student.scores
                    cls.score_compare(subscribe_student.openid, cur_student.sno,
                                      cls.base64decode(cur_student.passwd),
                                      cur_student.name, db_scores, subscribe_student)
                    subscribe_student.travel_nums = subscribe_student.travel_nums + 1
                    subscribe_student.save()
                    time.sleep(1)
                except Exception as e:
                    logger.error("遍历当前学生：%s失败! %s" % (subscribe_student, e))
            travel_end = time.time()
            logger.info("【成绩订阅】遍历%s个学生共耗时%ss" % (len(subscribe_students), travel_end - travel_begin))
        except Exception as e:
            logger.error("获取订阅的学生失败！ %s" % e)

    @classmethod
    def del_all_subscribe_students(cls):
        """
        遍历已经订阅的数据库表，去查找学号密码，挨个遍历，时间间隔十五分钟（多线程改进）
        :return:
        """
        try:
            # 找出已经订阅的student
            subscribe_students = models.SubscribeStudent.objects.all()
            subscribe_students_len = len(subscribe_students)
            subscribe_students.delete()
            logger.info("删除【%d】个订阅学生成功" % subscribe_students_len)
        except Exception as e:
            logger.error("获取订阅的学生失败！ %s" % e)

    @classmethod
    def update_score(cls, sno, passwd, subscribe_student):
        """
        """
        res = score.main(sno, passwd, "null")
        if res["message"] == "success" and res["have_class"] == 1:
            courses = res["courses"]
            try:
                db_write_scores = [course["score"] for course in courses]
                db_write_scores_str = cls.__list_to_str(db_write_scores)
                subscribe_student.sno = sno
                subscribe_student.scores = db_write_scores_str
                subscribe_student.save()
            except Exception as e:
                logger.error("[sno]: %s [passwd]: %s [定期更新订阅成绩列表异常]: [Exception]: %s" % (sno, passwd, e))
        else:
            logger.error("[sno]: %s [name]: %s [定期更新订阅成绩列表失败]: [reason]: %s" % (sno, passwd, res))

    @classmethod
    def update_all_subscribe_student(cls):
        """
        遍历已经订阅的数据库表，去查找学号密码，挨个遍历，更新当前的成绩，时间间隔半天
        :return:
        """
        try:
            # 找出已经订阅的student
            subscribe_students = models.SubscribeStudent.objects.all()
            # 遍历列表
            travel_begin = time.time()
            for subscribe_student in subscribe_students:
                try:
                    # 判断是否重新进行了登录
                    cur_student = models.Student.objects.filter(openid=subscribe_student.openid)[0]
                    cls.update_score(cur_student.sno, cls.base64decode(cur_student.passwd), subscribe_student)
                except Exception as e:
                    logger.error("[定期更新订阅成绩列表]遍历当前学生：%s失败! %s" % (subscribe_student, e))
            travel_end = time.time()
            logger.info("[定期更新订阅成绩列表]更新%s个学生课程成功，共耗时%ss" % (len(subscribe_students), travel_end - travel_begin))
        except Exception as e:
            logger.error("[定期更新订阅成绩列表]获取订阅的学生失败！ %s" % e)

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

    @classmethod
    def base64decode(cls, passwd):
        """数据库密码解密"""
        decode_passwd = base64.b64decode(passwd.encode('GBK')).decode('ascii')  # .decode('ascii') 转换成字符形式
        return decode_passwd


# if __name__ == '__main__':
#     AccessToken.update_access_token()
#     token1 = AccessToken.access_token
#     token2 = AccessToken.access_token
#     print(token1 == token2)
#     SubscribeScore.travel_subscribe_student()
    # ScoreSubscribe.send_score("oevr15Yuv8W4PvBsAgajC-BdVj8Q", "qinqinqin", "21180231272", "1001", "编译原理", "99.00")
