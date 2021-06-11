#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: qinchangshuai(cs_qin@qq.com) 
Date: 2021/1/16 9:04 
"""

import pdfplumber
import json

path = '../../static/exam_pdf/2021夏季期末.pdf'
pdf = pdfplumber.open(path)
tables = []
exams = {"english_up": {}, "english_down": {}, "professional_english": {},
         "english_down_jpan": {}, "english_down_e": {}, "professional_english_jpan": {},
         "professional_english_e": {}}
# df = pd.DataFrame(columns=['学号', '所属学院(中心）', '专业', '课程编号', '课程名称', '校区', '考场号', '座号', '教学楼', '教室', '考试时间'])
# df = df.append(pd.DataFrame(table[0][1:], columns=table[0][0]), ignore_index=True)
# , "makesi": {}, "zibian": {}, "english_up": {}, "english_down": {}, "professional_english": {}
course_name = set()
for page in pdf.pages:
    print(page)
    table = page.extract_tables()
    tables.append(table)
    print(table)
    for row in table[0][1:]:
        if row[5] == "中国特色社会主义理论与实践研究":
            exams["zhongte"][row[0]] = [row[0]] + row[2:]
        elif row[5] == "马克思主义与社会科学方法论":
            exams["makesi"][row[0]] = [row[0]] + row[2:]
        elif row[5] == "自然辩证法概论":
            exams["zibian"][row[0]] = [row[0]] + row[2:]
        elif row[5] == "研究生外国语(上)":
            exams["english_up"][row[0]] = [row[0]] + row[2:]
        elif row[5] == "研究生外国语(下)":
            exams["english_down"][row[0]] = [row[0]] + row[2:]
        elif row[5] == "专业学位研究生外国语":
            exams["professional_english"][row[0]] = [row[0]] + row[2:]
        elif row[5] == "研究生外国语(下)-日语":
            exams["english_down_jpan"][row[0]] = [row[0]] + row[2:]
        elif row[5] == "专业学位研究生外国语-日语":
            exams["professional_english_jpan"][row[0]] = [row[0]] + row[2:]
        elif row[5] == "专业学位研究生外国语-俄语":
            exams["professional_english_e"][row[0]] = [row[0]] + row[2:]
        elif row[5] == "研究生外国语(下)-俄语":
            exams["english_down_e"][row[0]] = [row[0]] + row[2:]
        else:
            print("啥也没有%s" % row)
        course_name.add(row[3])
print(len(tables))
print(course_name)
json_obj = json.dumps(exams, indent=4)  # indent参数是换行和缩进
json_file = open('english.json', 'w')
json_file.write(json_obj)
json_file.close()  # 最终写入的json文件格式:
# with open('zhongte.json', 'r') as f:
#     dic = json.load(fp=f)
#     print(dic)




