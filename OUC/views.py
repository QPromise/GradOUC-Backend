#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: cs_qin(cs_qin@qq.com)
Date: 2019/11/3 14:22
"""

import json
import time
from django.shortcuts import render
from django.http import HttpResponse as response

from .core import login, schedule, today_course, course, score, library, profile, school_course, score_subscribe, exam
from .news import yanzhao, xueshu, houqin, school, yanyuan
from .models import Config, News, Swiper


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


def index(request):
    return render(request, "profile.html")
    # return response('欢迎使用微信小程序【研在OUC】')


# 消息通知
def get_news(request):
    news = News.objects.all()[0]
    res = {"index": news.index, "news": news.news + "  发布时间:" + str(news.date).split()[0] + ""}
    # print(res)
    res = json.dumps(res)
    return response(res)


# 配置开学日期，放假日期，学年，学期
def get_config(request):
    res = Config.objects.all()[0]
    # print(res.begin_day)
    # 换成时间戳格式
    begin_day = time.strptime(res.begin_day, "%Y-%m-%d %H:%M:%S")
    begin_day = int(time.mktime(begin_day))
    # print(begin_day)
    res = {"begin_day": begin_day, "end_day": res.end_day, "xn": res.xn, "xq": res.xq, "is_open_subscribe": res.is_open_subscribe}
    res = json.dumps(res)
    return response(res)


# 获取推送
def get_swiper(request):
    swipers = Swiper.objects.all()
    res = []
    for swiper in swipers:
        temp = dict()
        temp["url"] = swiper.url
        temp["image"] = swiper.get_img_url()
        # print(swiper.url)
        # print(swiper.get_img_url())
        res.append(temp)
    res = json.dumps(res)
    # print(res)
    return response(res)


# 绑定学号密码
def do_login(request):
    sno, passwd = request.POST.get('sno'), request.POST.get('passwd')
    openid = request.POST.get('openid')
    print(openid)
    # print(request.POST.get('sno'))
    # print(request.POST.get('passwd'))
    temp = login.main(sno, passwd, openid)
    res = {'message': temp['message'], 'name': temp['name'], 'sno': sno, 'passwd': passwd}
    res = json.dumps(res)
    return response(res)


# 获取课表
def get_schedule(request):
    sno, passwd, zc, xn, xj = request.POST.get('sno'), request.POST.get('passwd'), \
                              request.POST.get('zc'), request.POST.get('xn'), request.POST.get('xj')
    openid = request.POST.get('openid')
    temp = schedule.main(sno, passwd, openid, zc, xj, xn)
    res = {"message": temp["message"], "schedule": temp["schedule"]}
    res = json.dumps(res)
    return response(res)


# 获取今日课表
def get_today_course(request):
    sno, passwd, zc, xn, xj, day = request.POST.get('sno'), request.POST.get('passwd'), request.POST.get('zc'),\
                                   request.POST.get('xn'), request.POST.get('xj'), request.POST.get('day')
    openid = request.POST.get('openid')
    temp = today_course.main(sno, passwd, openid, zc, xj, xn, day)
    res = {"message": temp["message"], "course": temp["course"]}
    res = json.dumps(res)
    return response(res)


# 获取考试安排
def get_exam(request):
    sno = request.POST.get('sno')
    temp = exam.main(sno)
    res = {"message": temp["message"], "exams": temp["exams"]}
    res = json.dumps(res)
    return response(res)


# 获取课程
def get_course(request):
    sno, passwd = request.POST.get('sno'), request.POST.get('passwd')
    openid = request.POST.get('openid')
    # print(sno,passwd)
    temp = course.main(sno, passwd, openid)
    res = {"message": temp["message"], "courses": temp["courses"], "unplanned_courses": temp["unplanned_courses"],
           "school_require_credit": temp["school_require_credit"], "select_credit": temp["select_credit"],
           "get_credit": temp["get_credit"], "have_class": temp["have_class"]}
    # print(res)
    res = json.dumps(res)
    return response(res)


# 获取成绩以及平均学分绩
def get_score(request):
    sno, passwd = request.POST.get('sno'), request.POST.get('passwd')
    openid = request.POST.get('openid')
    temp = score.main(sno, passwd, openid)
    res = json.dumps(temp)
    return response(res)


# 获取个人信息
def get_profile(request):
    sno, passwd = request.POST.get('sno'), request.POST.get('passwd')
    openid = request.POST.get('openid')
    temp = profile.main(sno, passwd, openid)
    res = {"message": temp["message"], "info": temp["info"], "have_info": temp["have_info"]}
    res = json.dumps(res)
    return response(res)


# 获取全校开课
def get_school_course(request):
    sno, passwd = request.POST.get('sno'), request.POST.get('passwd')
    openid = request.POST.get('openid')
    xn, xq = request.POST.get('xn'), request.POST.get('xq')
    pageId, kkyx = request.POST.get('pageId'), request.POST.get('kkyx')
    kcmc, jsxm = request.POST.get('kcmc'), request.POST.get('jsxm')
    temp = school_course.main(xn, xq, sno, passwd, openid, kkyx, kcmc, jsxm, pageId)
    res = {"message": temp["message"], "pages_count": temp["pages_count"], "number": temp["number"],
           "schoolCourses": temp["school_courses"], "have_course": temp["have_course"]}
    res = json.dumps(res)
    return response(res)


# 订阅出成绩通知
def subscribe_score(request):
    openid = request.GET.get('openid')
    res = score_subscribe.SubscribeScore.subscribe_score(openid)
    res = json.dumps(res)
    return response(res)


# 查看订阅状态
def get_subscribe_status(request):
    openid = request.GET.get('openid')
    res = score_subscribe.SubscribeScore.get_subscribe_status(openid)
    res = json.dumps(res)
    return response(res)


def set_failure_popup_false(request):
    openid = request.GET.get('openid')
    res = score_subscribe.SubscribeScore.set_failure_popup_false(openid)
    return response(json.dumps(res))


# 图书查询
def search_book(request):
    keyword, fieldCode, page = request.POST.get('keyword'), request.POST.get('type'), request.POST.get('page')
    temp = library.search_book(fieldCode, keyword, page)
    # print(temp)
    res = json.dumps(temp)
    return response(res)


# 获取图书详细信息
def get_bookDetail(request):
    bookID = request.POST.get('bookID')
    temp = library.get_bookDetail(bookID)
    # print(temp)
    res = {"have_info": temp["have_info"], "bookAvailableDetail": temp["bookAvailableDetail"]}
    res = json.dumps(temp)
    return response(res)


# 获取资讯
def get_schoolNews(request):
    type, page = request.POST.get('type'), request.POST.get('page')
    # 1001代表研招网
    if type == '1001':
        temp = yanzhao.get_news(page)
        res = {"pages_count": temp["pages_count"], "news": temp["total_news"]}
        res = json.dumps(res)
        return response(res)
    # 1002代表学术资讯
    elif type == '1002':
        temp = xueshu.get_news(page)
        res = {"pages_count": temp["pages_count"], "news": temp["total_news"]}
        res = json.dumps(res)
        return response(res)
    # 1003 代表后勤公告
    elif type == '1003':
        temp = houqin.get_news(page)
        res = {"pages_count": temp["pages_count"], "news": temp["total_news"]}
        res = json.dumps(res)
        return response(res)
    # 1004 代表学校新闻
    elif type == '1004':
        temp = school.get_news(page)
        res = {"pages_count": temp["pages_count"], "news": temp["total_news"]}
        res = json.dumps(res)
        return response(res)
    # 1005 代表研究生院新闻
    elif type == '1005':
        temp = yanyuan.get_news(page)
        res = {"pages_count": temp["pages_count"], "news": temp["total_news"]}
        res = json.dumps(res)
        return response(res)


# 获取资讯详细内容
def get_schoolNewsDetail(request):
    type, id = request.POST.get('type'), request.POST.get('id')
    res = None
    if type == '1001':
        res = yanzhao.get_newsDeatil(id)
    elif type == '1002':
        res = xueshu.get_newsDeatil(id)
    elif type == '1003':
        res = houqin.get_newsDeatil(id)
    elif type == '1004':
        res = school.get_newsDeatil(id)
    elif type == '1005':
        res = yanyuan.get_newsDeatil(id)
    return response(res)


def shenpi_submit(request):
    person_id = request.GET.get("vip")
    if person_id is None:
        return render(request, "shenpi_submit.html")
    else:
        person_dict = {
            "0": {"sno": "21180231272", "name": "秦昌帅"},
            "1": {"sno": "21200231213", "name": "王洁"},
            "2": {"sno": "21180231274", "name": "李健"},
        }
        return render(request, "shenpi_submit.html",
                      {"sno": person_dict[person_id]["sno"], "name": person_dict[person_id]["name"]})


def shenpi_index(request):
    doors = {"1": "崂山校区南门", "2": "崂山校区北门", "3": "崂山校区西门", "4": "崂山校区东门", "5": "南海苑", "6": "东海苑"}

    sno, name = request.POST.get("sno"), request.POST.get("name")
    out = request.POST.get("out")
    door_index = request.POST.get("door")
    type = request.POST.get("type")

    name = "小叮当" if name == "" else name
    avatar = "https://imgshenpi.ouc.edu.cn/avatarNew/%s.jpg" % sno if sno != "" \
        else "https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=4045261102,767704663&fm=26&gp=0.jpg"
    go = "出" if out == "1" else "入"

    if type == "1":
        return render(request, "shenpi_index.html",
                      {"avatar": avatar, "name": name, "go": go, "door": doors[door_index]})
    else:
        return render(request, "shenpi_index_teacher.html",
                      {"avatar": avatar, "name": name, "door": doors[door_index]})


