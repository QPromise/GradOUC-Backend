#!/usr/bin/python3
# _*_coding:utf-8 _*_

import time
import json
import bs4
import os
from bs4 import  BeautifulSoup

print(os.listdir("../OUC/static/exam_json/"))
cur = int(time.time())
end = 1610606871
print((end - cur) // (3600 * 24))
expire_time = time.strptime("2021-01-20 15:32:08", "%Y-%m-%d %H:%M:%S")
expire_time = int(time.mktime(expire_time))
print(2020 in range(2020, 2020))
print(",".join(list(map(str, ["计算机科学"]))))
print("http://grad.ouc.edu.cn/"[:-1])
a = ["自然辩证法", "中特", "英语"]
b = ["中特", "maogai", "自然辩证法"]
print(list(set(a).intersection(set(b))))
string = "[{'name': '自然辩证法概论', 'type': '公共课', 'credit': 1.0, 'score': 88.0, 'selected': True, 'disabled': False}, {'name': '中国特色社会主义理论与实践研究', 'type': '公共课', 'credit': 2.0, 'score': 94.0, 'selected': True, 'disabled': False}, {'name': '专业学位研究生外国语', 'type': '公共课', 'credit': 3.0, 'score': '免修', 'selected': False, 'disabled': True}, {'name': '工程伦理', 'type': '公共课', 'credit': 1.0, 'score': '未出', 'selected': False, 'disabled': True}, {'name': '学术道德与规范', 'type': '公共课', 'credit': 1.0, 'score': 98.0, 'selected': True, 'disabled': False}, {'name': '论文写作指导', 'type': '公共课', 'credit': 2.0, 'score': 91.0, 'selected': True, 'disabled': False}, {'name': '机器学习Ⅰ', 'type': '基础课', 'credit': 3.0, 'score': 89.0, 'selected': True, 'disabled': False}, {'name': '多媒体技术', 'type': '基础课', 'credit': 3.0, 'score': '未出', 'selected': False, 'disabled': True}, {'name': '三维计算机图形学', 'type': '专业课', 'credit': 3.0, 'score': 97.0, 'selected': True, 'disabled': False}, {'name': '图像处理与模式识别', 'type': '专业课', 'credit': 3.0, 'score': 91.5, 'selected': True, 'disabled': False}, {'name': '云计算', 'type': '其他课程', 'credit': 3.0, 'score': '未出', 'selected': False, 'disabled': True}, {'name': '多核处理与GPU计算', 'type': '其他课程', 'credit': 3.0, 'score': 99.0, 'selected': True, 'disabled': False}, {'name': '实践训练', 'type': '培养环节', 'credit': 6.0, 'score': '未选', 'selected': False, 'disabled': True}, {'name': '开题审核', 'type': '培养环节', 'credit': 0.0, 'score': '未选', 'selected': False, 'disabled': True}]"
json_str = json.dumps(string, ensure_ascii=False)
print(type(json_str))
print(json_str[0])
string = "[{'name': '自然辩证法概论', 'type': '公共课', 'credit': 1.0, 'score': 88.0, 'selected': True, 'disabled': False}, {'name': '中国特色社会主义理论与实践研究', 'type': '公共课', 'credit': 2.0, 'score': 94.0, 'selected': True, 'disabled': False}, {'name': '专业学位研究生外国语', 'type': '公共课', 'credit': 3.0, 'score': '免修', 'selected': False, 'disabled': True}, {'name': '工程伦理', 'type': '公共课', 'credit': 1.0, 'score': '未出', 'selected': False, 'disabled': True}, {'name': '学术道德与规范', 'type': '公共课', 'credit': 1.0, 'score': 98.0, 'selected': True, 'disabled': False}, {'name': '论文写作指导', 'type': '公共课', 'credit': 2.0, 'score': 91.0, 'selected': True, 'disabled': False}, {'name': '机器学习Ⅰ', 'type': '基础课', 'credit': 3.0, 'score': 89.0, 'selected': True, 'disabled': False}, {'name': '多媒体技术', 'type': '基础课', 'credit': 3.0, 'score': '未出', 'selected': False, 'disabled': True}, {'name': '三维计算机图形学', 'type': '专业课', 'credit': 3.0, 'score': 97.0, 'selected': True, 'disabled': False}, {'name': '图像处理与模式识别', 'type': '专业课', 'credit': 3.0, 'score': 91.5, 'selected': True, 'disabled': False}, {'name': '云计算', 'type': '其他课程', 'credit': 3.0, 'score': '未出', 'selected': False, 'disabled': True}, {'name': '多核处理与GPU计算', 'type': '其他课程', 'credit': 3.0, 'score': 99.0, 'selected': True, 'disabled': False}, {'name': '实践训练', 'type': '培养环节', 'credit': 6.0, 'score': '未选', 'selected': False, 'disabled': True}, {'name': '开题审核', 'type': '培养环节', 'credit': 0.0, 'score': '未选', 'selected': False, 'disabled': True}]"
json_str = eval(string)
print(type(json_str))
# print(begin_day)
#
# import requests
# s = requests.session()
# headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
#         'Connection': 'close'
#     }
# url = "http://www.baidu.com/"
# s.keep_alive = False
# s.proxies = {
#                 "http": "182.34.27.148:9999"
#              }
# r = s.get(url, headers=headers)
# profile_soup = BeautifulSoup(r.text, 'lxml')
# print(profile_soup)
# print(r.status_code)  # 如果代理可用则正常访问，不可用报以上错误