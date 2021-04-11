#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: qinchangshuai(cs_qin@qq.com) 
Date: 2021/4/8 14:56 
"""

from OUC import log

logger = log.logger
department_array = ['信息科学与工程学院', '海洋与大气学院', '化学化工学院', '海洋地球科学学院', '水产学院',
                    '海洋生命学院', '食品科学与工程学院', '医药学院', '工程学院', '环境科学与工程学院',
                    '数学科学学院', '管理学院', '经济学院', '外国语学院', '文学与新闻传播学院', '法学院',
                    '材料科学与工程学院', '马克思主义学院', '基础教学中心', '会计硕士教育中心',
                    '旅游管理硕士教育中心', '国际事务与公共管理学院', 'MBA教育中心', 'MPA教育中心']


def main():
    res = {"message": "success", "infos": [], "years": []}
    infos = []
    total = 0
    try:
        with open('OUC/static/post_graduate/info.txt', 'r', encoding="utf-8") as f:
            lines = f.readlines()
            years = lines[0].replace("\n", "").split("\t")[18:]
            pre = ""
            count = 0
            for i in range(1, len(lines)):
                cur_line = lines[i].replace("\n", "")
                split_line = cur_line.split("\t")
                if split_line[0] != pre:
                    if i != 1:
                        infos.append(cur_department)
                    total += count
                    pre = split_line[0]
                    count = 0
                    cur_department = dict()
                    cur_department["cur_department_professions"] = []
                cur_profession = dict()
                count += 1
                cur_department["department"] = split_line[0]
                cur_department["num"] = count
                try:
                    cur_profession["badge"] = "%s.png" % (department_array.index(split_line[0]) + 1)
                except:
                    cur_profession["badge"] = "0.png"
                cur_profession["department"] = split_line[0]  # 招生学院
                cur_profession["first_level_discipline"] = split_line[1]  # 一级学科
                cur_profession["second_level_discipline"] = split_line[2]  # 二级学科
                cur_profession["profession_type"] = split_line[3]  # 专硕or学硕
                cur_profession["tuition"] = split_line[4]  # 一年学费
                cur_profession["study_period"] = split_line[5]  # 专业学制
                cur_profession["first_test_political"] = split_line[6]  # 政治
                cur_profession["first_test_english"] = split_line[7]  # 英语
                cur_profession["first_test_profession_one"] = split_line[8]  # 业务课一
                cur_profession["first_test_profession_two"] = split_line[9]  # 业务课二
                cur_profession["retest_profession_one"] = split_line[10]  # 复试业务课一
                cur_profession["retest_profession_two"] = split_line[11]  # 复试业务课二
                cur_profession["first_test_books"] = split_words(split_line[12])
                cur_profession["first_test_books_version"] = split_words(split_line[13])
                cur_profession["first_test_books_imgs"] = split_words(split_line[14])
                cur_profession["retest_books"] = split_words(split_line[15])
                cur_profession["retest_books_version"] = split_words(split_line[16])
                cur_profession["retest_books_imgs"] = split_words(split_line[17])
                cur_profession["admission_ratio"] = split_words(split_line[18:])
                cur_profession["is_show"] = True
                cur_department["cur_department_professions"].append(cur_profession)
                judge_row_type_is_right(i + 1, [len(cur_profession["first_test_books"]),
                                                len(cur_profession["first_test_books_version"]),
                                                len(cur_profession["first_test_books_imgs"])],
                                                [len(cur_profession["retest_books"]),
                                                 len(cur_profession["retest_books_version"]),
                                                 len(cur_profession["retest_books_imgs"])],
                                                 cur_profession["admission_ratio"])
        infos.append(cur_department)
        total += count
        res["infos"] = infos
        res["years"] = years
        res["total"] = total
        return res
    except Exception as e:
        logger.error("获取信息异常: %s" % e)
        res["message"] = "fault"
        return res


def split_words(elements):
    if elements == "" or elements == "-":
        return []
    if type(elements) is str:
        return elements.split("#")
    if type(elements) is list:
        res = []
        for ele in elements:
            res.append(ele.split("#"))
        return res
    return []


def judge_row_type_is_right(row_num, cs_list, fs_list, bl_list):
    cs_info, fs_info, bl_info = "", "", ""
    for i in range(len(cs_list)):
        if i == 0:
            pre = cs_list[0]
        else:
            if cs_list[i] != pre:
                cs_info = "【初试参考书格式不正确】"
            else:
                pre = cs_list[i]

    for i in range(len(fs_list)):
        if i == 0:
            pre = fs_list[0]
        else:
            if fs_list[i] != pre:
                fs_info = "【复试参考书格式不正确】"
            else:
                pre = fs_list[i]

    for i in range(len(bl_list)):
        if len(bl_list[i]) != 5:
            bl_info = "【%s列复试报录信息格式不正确，缺少信息】" % (12 + i)
    if cs_info or fs_info or bl_info:
        logger.error("[%s行]%s%s%s" % (row_num, cs_info, fs_info, bl_info))


