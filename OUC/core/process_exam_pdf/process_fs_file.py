#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: qinchangshuai(cs_qin@qq.com) 
Date: 2021/4/16 18:32 
"""

import pdfplumber
import json
import xlsxwriter


# 需要对照复试成绩结果对复试名单进行筛选，适用于复试名单上不分二级专业的情况
def process_retest_list_by_sno(sno_file_path, write_file_path):
    with open(sno_file_path, 'r') as f:
        sno = f.readlines()
    for i in range(len(sno)):
        sno[i] = sno[i].strip()
    print(sno)
    find = [0] * len(sno)
    path = './files/2022fs.pdf'  # 复试文件
    pdf = pdfplumber.open(path)
    work_book = xlsxwriter.Workbook(write_file_path)
    work_sheet = work_book.add_worksheet()
    work_sheet.write(0, 0, "政治理论")
    work_sheet.write(0, 1, "外国语")
    work_sheet.write(0, 2, "业务课一")
    work_sheet.write(0, 3, "业务课二")
    work_sheet.write(0, 4, "总分")
    work_sheet.write(0, 5, "排名")
    work_sheet.write(0, 6, "状态")
    tables = []
    rank = 1

    for page in pdf.pages:
        table = page.extract_tables()
        tables.append(table)
        for row in table[0][1:]:
            if row[0] in sno:
                print(sno.index(row[0]))
                find[sno.index(row[0])] = 1
                work_sheet.write(rank, 0, row[5])
                work_sheet.write(rank, 1, row[6])
                work_sheet.write(rank, 2, row[7])
                work_sheet.write(rank, 3, row[8])
                work_sheet.write(rank, 4, row[9])
                work_sheet.write(rank, 5, rank)
                work_sheet.write(rank, 6, row[10])
                # lines.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (row[5], row[6], row[7], row[8], row[9], rank, row[10]))
                rank += 1
    work_book.close()
    # with open('./files/2021-1.txt', encoding="utf-8", mode='w+') as f:
    #     f.writelines(lines)

    for i in range(len(find)):
        if find[i] == 0:
            print(sno[i])


# 输入专业，根据最原始复试文件提取复试人员的成绩等
def process_retest_list_original(write_file_name, profession_code_list):
    path = './files/2022fs.pdf'
    pdf = pdfplumber.open(path)
    work_book = xlsxwriter.Workbook('./files/' + write_file_name + '.xls')
    work_sheet = work_book.add_worksheet()
    work_sheet.write(0, 0, "政治理论")
    work_sheet.write(0, 1, "外国语")
    work_sheet.write(0, 2, "业务课一")
    work_sheet.write(0, 3, "业务课二")
    work_sheet.write(0, 4, "总分")
    work_sheet.write(0, 5, "排名")
    work_sheet.write(0, 6, "状态")
    tables = []
    rank = 1
    tmp_rows = []
    for page in pdf.pages:
        print(page)
        table = page.extract_tables()
        tables.append(table)
        # print(tables)
        for row in table[0][1:]:
            print(row[4])
            if row[3].replace("\n", "") in profession_code_list:
                tmp_row = [""] * 6
                tmp_row[0] = row[5]
                tmp_row[1] = row[6]
                tmp_row[2] = row[7]
                tmp_row[3] = row[8]
                tmp_row[4] = row[9]
                tmp_row[5] = row[10]
                tmp_rows.append(tmp_row)
    tmp_rows = sorted(tmp_rows, key=lambda x: x[4], reverse=True)
    for i in range(len(tmp_rows)):
        work_sheet.write(rank, 0, tmp_rows[i][0])
        work_sheet.write(rank, 1, tmp_rows[i][1])
        work_sheet.write(rank, 2, tmp_rows[i][2])
        work_sheet.write(rank, 3, tmp_rows[i][3])
        work_sheet.write(rank, 4, tmp_rows[i][4])
        work_sheet.write(rank, 5, rank)
        work_sheet.write(rank, 6, tmp_rows[i][5])
        rank += 1
    work_book.close()


if __name__ == '__main__':
    # tes_camelot()
    process_retest_list_by_sno("./files/fs/input/12", "./files/fs/output/2022-12.xls")
    # process_retest_list_original("2022-7", ["083500"])




