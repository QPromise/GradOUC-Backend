"""
_*_coding:utf-8 _*_

@Time    :2019/11/3 14:22
@Author  :csqin
@FileName: views.py
@Software: PyCharm

"""
from django.shortcuts import render
from django.http import HttpResponse as response
from .core import login,schedule,course,score,library
import json
from .models import Config,News
import time


# 消息通知
def get_news(request):
    news = News.objects.all()[0]
    res = {"index":news.index,"news":news.news+"  发布时间:"+str(news.date).split()[0]+""}
    print(res)
    res = json.dumps(res)
    return response(res)

# 配置开学日期，放假日期，学年，学期
def get_config(request):
    res = Config.objects.all()[0]
    print(res.begin_day)
    # 换成时间戳格式
    begin_day = time.strptime(res.begin_day, "%Y-%m-%d %H:%M:%S")
    begin_day = int(time.mktime(begin_day))
    print(begin_day)
    res = {"begin_day":begin_day,"end_day":res.end_day,"xn":res.xn,"xq":res.xq}
    res = json.dumps(res)
    return response(res)

# 绑定学号密码
def do_login(request):
    sno,passwd = request.POST.get('sno'),request.POST.get('passwd')
    print(request.POST.get('sno'))
    print(request.POST.get('passwd'))
    temp = login.main(sno,passwd)
    res = {'message':temp['message'],'name':temp['name'],'sno':sno,'passwd':passwd}
    res = json.dumps(res)
    return response(res)

# 获取课表
def get_schedule(request):
    sno, passwd,zc,xn,xj= request.POST.get('sno'), request.POST.get('passwd'),\
                          request.POST.get('zc'),request.POST.get('xn'),request.POST.get('xj')
    print(sno,passwd,zc,xn,xj)
    temp = schedule.main(sno,passwd,zc,xj,xn)
    res = {"message":temp["message"],"schedule":temp["schedule"]}
    res = json.dumps(res)
    return response(res)

# 获取课程
def get_course(request):
    sno, passwd = request.POST.get('sno'), request.POST.get('passwd')
    print(sno,passwd)
    temp = course.main(sno,passwd)
    res = {"message":temp["message"],"courses":temp["courses"],"have_class":temp["have_class"]}
    print(res)
    res = json.dumps(res)
    return response(res)

# 获取成绩以及平均学分绩
def get_score(request):
    sno, passwd = request.POST.get('sno'), request.POST.get('passwd')
    print(sno, passwd)
    temp = score.main(sno, passwd)
    res = {"message": temp["message"], "courses": temp["courses"], "mean":temp["mean"],"have_class": temp["have_class"]}
    res = json.dumps(res)
    return response(res)

# 图书查询
def search_book(request):
    keyword,fieldCode,page= request.POST.get('keyword'),request.POST.get('type'),request.POST.get('page')
    temp = library.search_book(fieldCode,keyword,page)
    # print(temp)
    res = json.dumps(temp)
    return response(res)
def get_bookDetail(request):
    bookID = request.POST.get('bookID')
    temp = library.get_bookDetail(bookID)
    print(temp)
    res = {"have_info":temp["have_info"],"bookAvailableDetail":temp["bookAvailableDetail"]}
    res = json.dumps(temp)
    return response(res)

