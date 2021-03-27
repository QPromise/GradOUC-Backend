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

from .core import login, schedule, today_course, course, score, library,\
    profile, school_course, score_subscribe, exam, recently_use, score_rank,\
    reward_files
from OUC.core import school_news
from .models import Config, News, Swiper


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


def index(request):
    return render(request, "profile.html")
    # return response('欢迎使用微信小程序【研在OUC】')


# =================================消息通知模块================================== #
# 消息通知
def get_news(request):
    news = News.objects.all()[0]
    res = {"index": news.index, "news": news.news + "  发布时间:" + str(news.date).split()[0] + ""}
    # print(res)
    res = json.dumps(res)
    return response(res)


# =================================全局配置模块================================== #
# 配置开学日期，放假日期，学年，学期
def get_config(request):
    res = Config.objects.all()[0]
    # print(res.begin_day)
    # 换成时间戳格式
    begin_day = time.strptime(res.begin_day, "%Y-%m-%d %H:%M:%S")
    begin_day = int(time.mktime(begin_day))
    # print(begin_day)
    res = {"begin_day": begin_day, "end_day": res.end_day, "xn": res.xn, "xq": res.xq, "is_open_subscribe": res.is_open_subscribe,
           "get_score_rank_nj_min": res.get_score_rank_nj_min, "get_score_rank_nj_max": res.get_score_rank_nj_max}
    res = json.dumps(res)
    return response(res)


# =================================banner图推送模块================================== #
# 获取推送
def get_swiper(request):
    swipers = Swiper.objects.all()
    res = []
    for swiper in swipers:
        temp = dict()
        temp["url"] = swiper.url
        temp["image"] = swiper.get_img_url()
        res.append(temp)
    res = json.dumps(res[::-1])
    # print(res)
    return response(res)


# =================================最近使用同学展示模块================================== #
# 获取最近使用的同学
def get_recently_use(request):
    openid = request.GET.get('openid')
    res = recently_use.main(openid)
    res = json.dumps(res)
    return response(res)


# =================================绑定登录模块================================== #
# 绑定学号密码
def do_login(request):
    sno, passwd = request.POST.get('sno'), request.POST.get('passwd')
    openid = request.POST.get('openid')
    # print(openid)
    # print(request.POST.get('sno'))
    # print(request.POST.get('passwd'))
    temp = login.main(sno, passwd, openid)
    res = {'message': temp['message'], 'name': temp['name'], 'sno': sno, 'passwd': passwd}
    res = json.dumps(res)
    return response(res)


# =================================我的课表模块================================== #
# 获取课表
def get_schedule(request):
    sno, passwd, zc, xn, xj = request.POST.get('sno'), request.POST.get('passwd'), \
                              request.POST.get('zc'), request.POST.get('xn'), request.POST.get('xj')
    openid = request.POST.get('openid')
    temp = schedule.main(sno, passwd, openid, zc, xj, xn)
    res = {"message": temp["message"], "schedule": temp["schedule"]}
    res = json.dumps(res)
    return response(res)


# =================================今日课表模块================================== #
# 获取今日课表
def get_today_course(request):
    sno, passwd, zc, xn, xj, day = request.POST.get('sno'), request.POST.get('passwd'), request.POST.get('zc'),\
                                   request.POST.get('xn'), request.POST.get('xj'), request.POST.get('day')
    openid = request.POST.get('openid')
    temp = today_course.main(sno, passwd, openid, zc, xj, xn, day)
    res = {"message": temp["message"], "course": temp["course"]}
    res = json.dumps(res)
    return response(res)


# =================================我的考试安排模块================================== #
# 获取考试安排
def get_exam(request):
    sno, my_sno, my_passwd, my_openid = request.POST.get('sno'), request.POST.get('my_sno'),\
                                        request.POST.get('my_passwd'), request.POST.get('my_openid')
    temp = exam.main(sno, my_sno, my_passwd, my_openid)
    res = {"message": temp["message"], "exams": temp["exams"]}
    res = json.dumps(res)
    return response(res)


# =================================我的课程模块================================== #
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


# =================================我的成绩模块================================== #
# 获取成绩以及平均学分绩
def get_score(request):
    sno, passwd = request.POST.get('sno'), request.POST.get('passwd')
    openid = request.POST.get('openid')
    temp = score.main(sno, passwd, openid)
    res = json.dumps(temp)
    return response(res)


# =================================个人信息模块================================== #
# 获取个人信息
def get_profile(request):
    sno, passwd = request.POST.get('sno'), request.POST.get('passwd')
    openid = request.POST.get('openid')
    temp = profile.main(sno, passwd, openid)
    res = {"message": temp["message"], "info": temp["info"], "have_info": temp["have_info"]}
    res = json.dumps(res)
    return response(res)


# =================================全校开课模块================================== #
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


# =================================成绩排名模块================================== #
# 查看成绩排名
def get_score_rank(request):
    openid, sno, passwd, type = request.GET.get('openid'), request.GET.get('sno'), request.GET.get('passwd'), request.GET.get('type')
    res = score_rank.ScoreRank.get_my_score_rank(openid, sno, passwd, type)
    res = json.dumps(res)
    return response(res)


# 更新平均学分绩
def update_avg_score(request):
    openid, sno, passwd = request.GET.get('openid'), request.GET.get('sno'), request.GET.get('passwd')
    res = score_rank.ScoreRank.update_my_score(openid, sno, passwd)
    res = json.dumps(res)
    return response(res)


def get_department_all_research(request):
    openid, sno = request.GET.get('openid'), request.GET.get('sno')
    res = score_rank.ScoreRank.get_department_all_research(openid, sno)
    res = json.dumps(res)
    return response(res)


def set_join_rank_research(request):
    openid, research_list = request.POST.get('openid'), request.POST.get('research_list')
    res = score_rank.ScoreRank.set_join_rank_research(openid, research_list)
    res = json.dumps(res)
    return response(res)


def get_common_courses(request):
    openid, sno = request.GET.get('openid'), request.GET.get('sno')
    res = score_rank.ScoreRank.get_commom_courses(openid, sno)
    res = json.dumps(res)
    return response(res)


def set_exclude_courses(request):
    openid, select_common_courses = request.POST.get('openid'), request.POST.get('select_common_courses')
    res = score_rank.ScoreRank.set_exclude_courses(openid, select_common_courses)
    res = json.dumps(res)
    return response(res)

# =================================成绩订阅模块================================== #
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


# =================================图书馆模块================================== #
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


# =================================校园资讯模块================================== #
# 获取资讯
def get_schoolNews(request):
    type, page = request.POST.get('type'), request.POST.get('page')
    temp = school_news.SchoolNews.get_news(str(type), str(page))
    res = {"pages_count": temp["pages_count"], "news": temp["total_news"]}
    res = json.dumps(res)
    return response(res)


# 获取资讯详细内容
def get_schoolNewsDetail(request):
    type, id = request.POST.get('type'), request.POST.get('id')
    res = school_news.SchoolNews.get_news_detail(str(type), str(id))
    return response(res)


# =================================获取奖学金文件模块================================== #
def get_reward_files(request):
    res = reward_files.main()
    res = json.dumps(res)
    return response(res)

# =================================moniqingjia模块================================== #
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


