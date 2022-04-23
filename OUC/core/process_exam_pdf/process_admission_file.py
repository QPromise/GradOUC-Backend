#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: qinchangshuai(cs_qin@qq.com) 
Date: 2021/4/29 13:51 
"""

import pdfplumber
import json
import xlsxwriter
import pandas as pd
import os


# 判断当前复试结果的考生编号是否被拟录取，输出加一列状态 1录取 2未录取
def get_retest_status_from_admission(retest_score_file_path, output_file_path, admission_sno_list):
    # 建立输出表格
    work_book = xlsxwriter.Workbook(output_file_path)
    work_sheet = work_book.add_worksheet()
    work_sheet.write(0, 0, "初试成绩")
    work_sheet.write(0, 1, "复试成绩")
    work_sheet.write(0, 2, "总成绩")
    work_sheet.write(0, 3, "状态")
    rank = 1

    # 读取带成绩和学号的复试成绩公示 ---- 考生编号/初试成绩/复试成绩/总成绩
    sheet = pd.read_excel(retest_score_file_path, "Sheet1")
    sheet_content = sheet.values.tolist()
    for i in range(len(sheet_content)):
        try:
            work_sheet.write(rank, 0, float(sheet_content[i][1]))
            work_sheet.write(rank, 1, float(sheet_content[i][2]))
            work_sheet.write(rank, 2, float(sheet_content[i][3]))
        except Exception as e:
            print("第%s行数字有误[%s, %s, %s] | %s" % (i + 1, sheet_content[i][1], sheet_content[i][2], sheet_content[i][3], e))
        # 未录取
        if str(int(sheet_content[i][0])).strip() not in admission_sno_list:
            print(int(sheet_content[i][0]))
            work_sheet.write(rank, 3, 2)
        # 录取
        else:
            work_sheet.write(rank, 3, 1)
        rank += 1
    work_book.close()


def get_admission_sno_list(admission_file_path, department_name):
    # 读取拟录取名单pdf提取拟录取考生编号
    pdf = pdfplumber.open(admission_file_path)
    tables, admission_sno_list = [], []
    for page in pdf.pages:
        table = page.extract_tables()
        tables.append(table)
        for row in table[0][1:]:
            # if row[2].replace("\n", "") == department_name:
            print(row[0], row[1])
            admission_sno_list.append(row[0].replace("\n", ""))
    print(len(admission_sno_list))
    return admission_sno_list


if __name__ == '__main__':
    # 获取被拟录取的sno list
    # sno_list = get_admission_sno_list('./files/niluqu/input/2022/22信息科学与工程学部拟录取名单.pdf', '信息科学与工程学部')
    with open('./files/niluqu/input/admission_sno_list.txt', 'r') as f:
        sno_list = f.readlines()
    for i in range(len(sno_list)):
        sno_list[i] = sno_list[i].strip()
    print(len(sno_list), sno_list)
    target_file_list = os.listdir('./files/niluqu/input/2022')
    print(target_file_list)
    for i in range(len(target_file_list)):
        num = target_file_list[i][0:2] if target_file_list[i][1] >= "0" and target_file_list[i][1] <= "9" else target_file_list[i][0]
        get_retest_status_from_admission('./files/niluqu/input/2022/' + target_file_list[i],
                                        './files/niluqu/output/2022/2022-' + num + '.xls',
                                         sno_list)