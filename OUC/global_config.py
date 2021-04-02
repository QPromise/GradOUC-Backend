#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: qinchangshuai(cs_qin@qq.com) 
Date: 2021/1/27 13:09 
"""
from fake_useragent import UserAgent
ua = UserAgent()

# =================================全局参数================================== #

# headers={
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     "Accept-Encoding": "gzip, deflate",
#     "Accept-Language": "zh-CN,zh;q=0.9",
#     "Cache-Control": "max-age=0",
#     "Connection": "close",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
# }
user_agent = ua.random
headers = {
        "User-Agent": user_agent,
        "Connection": "close",
        "Accept-Encoding": "Gzip",  # 使用gzip压缩传输数据让访问更快
}

# =================================登录模块================================== #
# 登录地址
login_url = "http://id.ouc.edu.cn:8071/sso/login?service=http%3A%2F%2Fpgs.ouc.edu.cn%2Fallogene%2Fpage%2Fhome.htm"
new_login_url = "http://pgs.ouc.edu.cn/sso/login?service=http%3A%2F%2Fpgs.ouc.edu.cn%2Fallogene%2Fpage%2Fhome.htm"
# 登录后主页
home_url = "http://pgs.ouc.edu.cn/allogene/page/home.htm"
# profile
profile_url = "http://pgs.ouc.edu.cn/py/page/student/ckgrxxjh.htm"

# =================================我的课程================================== #
# 课程地址
course_url = "http://pgs.ouc.edu.cn/py/page/student/grkcgl.htm"

# =================================我的课表================================== #
# 课表地址
schedule_url = "http://pgs.ouc.edu.cn/py/page/student/grkcb.htm"

# =================================学校开课================================== #
# 课程地址
school_course_url = "http://pgs.ouc.edu.cn/py/page/student/lnsjCxdc.htm"

# =================================校园资讯================================== #
houqin_url = "http://hqbzc.ouc.edu.cn/1670/list%s.htm"
school_url = "http://www.ouc.edu.cn/xsdt/list%s.htm"
xueshu_url = "http://www.ouc.edu.cn/xshd/list%s.htm"
yanyuan_url = "http://grad.ouc.edu.cn/13024/list%s.htm"
yanzhao_url = "http://yz.ouc.edu.cn/5926/list%s.htm"

houqin_detail_url = "http://hqbzc.ouc.edu.cn"
school_detail_url = "http://www.ouc.edu.cn"
xueshu_detail_url = "http://www.ouc.edu.cn"
yanyuan_detail_url = "http://grad.ouc.edu.cn/"
yanzhao_detail_url = "http://yz.ouc.edu.cn"