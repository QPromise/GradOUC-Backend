#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: qinchangshuai(cs_qin@qq.com) 
Date: 2021/4/8 14:56 
"""

import pandas as pd
import json
import collections

from OUC import log

logger = log.logger
department_array = ['信息科学与工程学部', '海洋与大气学院', '化学化工学院', '海洋地球科学学院', '水产学院',
                    '海洋生命学院', '食品科学与工程学院', '医药学院', '工程学院', '环境科学与工程学院',
                    '数学科学学院', '管理学院', '经济学院', '外国语学院', '文学与新闻传播学院', '法学院',
                    '材料科学与工程学院', '马克思主义学院', '基础教学中心', '会计硕士教育中心',
                    '旅游管理硕士教育中心', '国际事务与公共管理学院', 'MBA教育中心', 'MPA教育中心']

qq_qun = ['963707614', '963707614', '1048603730', '963707614', '963707614',
          '963707614', '963707614', '963707614', '963707614', '963707614',
          '963707614', '945610403', '945610403', '811731005', '963707614', '963707614',
          '963707614', '963707614', '963707614', '963707614',
          '963707614', '963707614', '963707614', '963707614']


def main():
    res = {"message": "success", "infos": [], "years": []}
    infos = []
    total = 0
    try:
        with open('OUC/static/post_graduate/info.txt', 'r', encoding="utf-8") as f:
            lines = f.readlines()
            years = lines[0].replace("\n", "").split("\t")[30:]
            pre = ""
            count = 0
            for i in range(1, len(lines)):
                cur_line = lines[i].replace("\n", "")
                split_line = cur_line.split("\t")
                if split_line[0] != pre:
                    if i != 1:
                        cur_department["cur_department_professions"] = sorted(cur_department["cur_department_professions"], key=lambda x: x['profession_type'])
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
                    cur_profession["badge"] = "%s.png" % (department_array.index(cur_department["department"]) + 1)
                    cur_profession["qq_qun"] = qq_qun[department_array.index(cur_department["department"])]
                except:
                    cur_profession["qq_qun"] = ""
                cur_profession["department"] = split_line[0]  # 招生学院
                cur_profession["campus"] = split_line[1]  # 所在校区

                cur_profession["first_level_discipline"] = split_line[2]  # 一级学科
                cur_profession["second_level_discipline_code"] = split_line[3]  # 二级学科
                cur_profession["second_level_discipline"] = split_line[4]  # 二级学科
                cur_profession["profession_type"] = split_line[5]  # 专硕or学硕
                cur_profession["tuition"] = split_line[6]  # 一年学费
                cur_profession["rank_mode"] = split_line[7]  # 排名方式

                cur_profession["study_period"] = split_line[8]  # 专业学制
                cur_profession["profession_introduction"] = split_line[9]  # 专业介绍

                cur_profession["first_test_political"] = split_line[10]  # 政治
                cur_profession["first_test_english"] = split_line[11]  # 英语
                cur_profession["first_test_profession_one"] = split_line[12]  # 业务课一
                cur_profession["first_test_profession_two"] = split_line[13]  # 业务课二
                cur_profession["retest_profession_one"] = split_line[14]  # 复试业务课一
                cur_profession["retest_profession_two"] = split_line[15]  # 复试业务课二

                cur_profession["first_test_books"] = split_words(split_line[16])
                cur_profession["first_test_books_author"] = split_words(split_line[17])
                cur_profession["first_test_books_version"] = split_words(split_line[18])
                cur_profession["first_test_books_publish_hourses"] = split_words(split_line[19])
                cur_profession["first_test_books_introduction"] = split_words(split_line[20])
                cur_profession["first_test_books_imgs"] = add_book_img_dir_prefix(split_words(split_line[21]), cur_department["department"])

                cur_profession["retest_books"] = split_words(split_line[22])
                cur_profession["retest_books_author"] = split_words(split_line[23])
                cur_profession["retest_books_version"] = split_words(split_line[24])
                cur_profession["retest_books_publish_hourses"] = split_words(split_line[25])
                cur_profession["retest_books_introduction"] = split_words(split_line[26])
                cur_profession["retest_books_imgs"] = add_book_img_dir_prefix(split_words(split_line[27]), cur_department["department"])

                cur_profession["admission_list_files"] = get_file_list(split_words(split_line[28]),  # 拟录取名单
                                                                              cur_department["department"])
                cur_profession["retest_list_files"] = get_file_list(split_words(split_line[29]),  # 复试名单
                                                                    cur_department["department"])

                cur_profession["admission_ratio"] = split_words(split_line[30:])
                cur_profession["is_show"] = True
                cur_department["cur_department_professions"].append(cur_profession)
                judge_row_type_is_right(i + 1, [len(cur_profession["first_test_books"]),
                                                len(cur_profession["first_test_books_author"]),
                                                len(cur_profession["first_test_books_version"]),
                                                len(cur_profession["first_test_books_publish_hourses"]),
                                                len(cur_profession["first_test_books_introduction"]),
                                                len(cur_profession["first_test_books_imgs"]),
                                                ],
                                                [len(cur_profession["retest_books"]),
                                                 len(cur_profession["retest_books_author"]),
                                                 len(cur_profession["retest_books_version"]),
                                                 len(cur_profession["retest_books_publish_hourses"]),
                                                 len(cur_profession["retest_books_introduction"]),
                                                 len(cur_profession["retest_books_imgs"])
                                                 ],
                                                 cur_profession["admission_ratio"])
        cur_department["cur_department_professions"] = sorted(cur_department["cur_department_professions"],
                                                              key=lambda x: x['profession_type'])
        infos.append(cur_department)
        total += count
        # res["infos"] = infos
        res["years"] = years
        # res["total"] = total
        return res
    except Exception as e:
        logger.error("获取信息异常: %s" % e)
        res["message"] = "fault"
        return res


def split_words(elements):
    """
    按#拆分单元格数据，没有数据为-，可能是列表或者字符串类型
    :param elements:
    :return:
    """
    if elements == "" or elements == "-":
        return []
    if type(elements) is str:
        return elements.split("#")
    if type(elements) is list:
        res = []
        for ele in elements:
            if ele != "-" and ele != "":
                res.append(ele.split("#"))
        return res
    return []


def add_book_img_dir_prefix(imgs, department):
    """
    添加书籍图片前缀
    :param imgs:
    :param department:
    :return:
    """
    if len(imgs) == 0:
        return []
    for i in range(len(imgs)):
        if imgs[i] != "-":
            imgs[i] = "%s/%s" % (department, imgs[i])
    return imgs


def get_file_list(files, department):
    """
    获取名单列表
    :param files:
    :param department:
    :return:
    """
    if len(files) == 0:
        return []
    res = []
    for i in range(len(files)):
        cur_file = dict()
        if files[i] != "-":
            cur_file["val"] = "/%s/%s/%s" % (department, get_year(files[i]), files[i])
            cur_file["btnname"] = get_year(files[i])
        else:
            cur_file["val"] = "-"
            cur_file["btnname"] = "-"
        res.append(cur_file)
    return res


def get_year(element):
    """
    获取复试名单年份
    :param element:
    :return:
    """
    return element.split("-")[0]


def judge_row_type_is_right(row_num, cs_list, fs_list, bl_list):
    """
    判断格式是否合法
    :param row_num:  第几行
    :param cs_list: 初试列表
    :param fs_list: 复试列表
    :param bl_list: 报录比列表
    :return:
    """
    cs_info, fs_info, bl_info = "", "", ""
    cs_len = len(list(set(cs_list)))
    if cs_len != 1 and 0 not in cs_list:
        cs_info = "【初试参考书格式不正确 | %s】" % cs_list

    fs_len = len(list(set(fs_list)))
    if fs_len != 1 and 0 not in fs_list:
        fs_info = "【复试参考书格式不正确 | %s】" % fs_list

    for i in range(len(bl_list)):
        if len(bl_list[i]) != 5:
            bl_info = "【%s列复试报录信息格式不正确，缺少信息】" % (24 + i)
    if cs_info or fs_info or bl_info:
        pass
        # logger.error("[%s行]%s%s%s" % (row_num, cs_info, fs_info, bl_info))


# 读取复试名单
def read_retest_list(retest_list_files):
    """
    根据文件名称加载当前的复试名单
    政治理论	外国语	业务课一	业务课二	总分	排名	状态
    政治理论	外国语	业务课一	业务课二	总分	专业    排名	状态
    """
    res = {"message": "success", "each_year_retest_file": {}}
    # sheet = pd.read_excel("OUC/static/post_graduate/retest_list_files" + file_name, "Sheet1")
    try:
        for i in range(len(retest_list_files)):
            if retest_list_files[i]["val"] == "-":
                continue
            try:
                sheet = pd.read_excel("OUC/static/post_graduate/retest_list_files" + retest_list_files[i]["val"], "Sheet1")
            except Exception as e:
                logger.error("%s %s不存在" % (e, retest_list_files[i]["val"]))
                continue
            # sheet = pd.read_excel("../../static/post_graduate/retest_list_files" + file_name, "Sheet1")
            cur_year = {"th": [], "rows": [], "analysis_th": [], "analysis_rows": []}
            columns = sheet.columns.tolist()
            has_status = False
            if columns[-1] == "状态":
                th = columns[:-1]
                has_status = True
            else:
                th = columns
            mean, max_score, min_score = ["平均值"], ["最高分"], ["最低分"]
            for j in range(5):
                mean.append(round(sheet[th[j]].mean().tolist(), 1))
                max_score.append(sheet[th[j]].max().tolist())
                min_score.append(sheet[th[j]].min().tolist())
            content = sheet.values.tolist()
            rows = []
            discipline_description = []
            if columns[5] != "专业":
                for j in range(len(content)):
                    row = dict()
                    # 如果有标记
                    if has_status:
                        if pd.isnull(content[j][-1]):
                            row["status"] = 1
                        else:
                            row["status"] = int(content[j][-1])
                        row["val"] = content[j][:-1]
                    else:
                        row["status"] = 1
                        row["val"] = content[j]
                    rows.append(row)
            else:
                second_level_discipline_list = sheet[columns[5]].tolist()
                second_level_discipline_dict = collections.OrderedDict()  # list(set(sheet[columns[5]].tolist()))
                flag = 1
                for ele in second_level_discipline_list:
                    if second_level_discipline_dict.get(ele) is None:
                        second_level_discipline_dict[ele] = flag
                        flag += 1
                    else:
                        pass
                discipline_description = ["%s - %s" % (v, k) for k, v in second_level_discipline_dict.items()]
                for j in range(len(content)):
                    row = dict()
                    # 如果有标记
                    if has_status:
                        if pd.isnull(content[j][-1]):
                            row["status"] = 1
                        else:
                            row["status"] = int(content[j][-1])
                        row["val"] = content[j][:5] + [second_level_discipline_dict[second_level_discipline_list[j]]] + content[j][6:-1]
                    else:
                        row["status"] = 1
                        row["val"] = content[j][:5] + [second_level_discipline_dict[second_level_discipline_list[j]]] + content[j][6:]
                    rows.append(row)
            cur_year["discipline_description"] = discipline_description
            cur_year["rows"] = rows
            cur_year["th"] = th
            cur_year["analysis_th"] = ["指标"] + th[:5]
            cur_year["analysis_rows"] = [mean, max_score, min_score]
            cur_year["length"] = len(rows)
            res["each_year_retest_file"][retest_list_files[i]["btnname"]] = cur_year
        if res["each_year_retest_file"] == {}:
            res["message"] = "empty"
        return res
    except Exception as e:
        res["message"] = "fault"
        logger.error("%s" % e)
        return res


def read_admission_list(admission_list_files):
    """
    根据文件名称加载当前的复试名单
    """
    res = {"message": "success", "each_year_admission_file": {}}
    # sheet = pd.read_excel("OUC/static/post_graduate/admission_list_files" + file_name, "Sheet1")
    try:
        for i in range(len(admission_list_files)):
            if admission_list_files[i]["val"] == "-":
                continue
            try:
                sheet = pd.read_excel("OUC/static/post_graduate/admission_list_files" + admission_list_files[i]["val"], "Sheet1")
            except Exception as e:
                logger.error("%s %s不存在" % (e, admission_list_files[i]["val"]))
                continue
            cur_year = {"th": [], "rows": []}
            columns = sheet.columns.tolist()
            # 初试成绩排序
            first_test_score = sheet[columns[0]].tolist()
            sorted_first_test_score = sorted(first_test_score, reverse=True)
            # 总成绩
            score = sheet[columns[2]].tolist()
            # 成绩波动
            rank_change = []
            for j in range(len(score)):
                change = sorted_first_test_score.index(first_test_score[j]) - j
                if change > 0:
                    change = "+" + str(change)
                rank_change.append(change)
            content = sheet.values.tolist()
            rows = []
            admission_num = 0
            for j in range(len(content)):
                row = dict()
                # 如果没有标记
                if pd.isnull(content[j][-1]):
                    row["status"] = 1
                else:
                    row["status"] = int(content[j][-1])
                if row["status"] == 1:
                    admission_num += 1
                row["val"] = content[j][:-1] + [rank_change[j]]
                rows.append(row)
            cur_year["rows"] = rows
            cur_year["th"] = columns[:-1] + ['名次变动']
            cur_year["length"] = admission_num
            res["each_year_admission_file"][admission_list_files[i]["btnname"]] = cur_year
        if res["each_year_admission_file"] == {}:
            res["message"] = "empty"
        return res
    except Exception as e:
        res["message"] = "fault"
        logger.error("%s" % e)
        return res


def test_file(file_name):
    sheet = pd.read_excel("../../static/post_graduate/retest_list_files" + file_name, "Sheet1")
    cur_year = {"th": [], "rows": [], "analysis_th": [], "analysis_rows": []}
    columns = sheet.columns.tolist()
    has_status = False
    if columns[-1] == "状态":
        th = columns[:-1]
        has_status = True
    else:
        th = columns
    mean, max_score, min_score = ["平均值"], ["最高分"], ["最低分"]
    for j in range(5):
        mean.append(round(sheet[th[j]].mean().tolist(),1))
        max_score.append(sheet[th[j]].max().tolist())
        min_score.append(sheet[th[j]].min().tolist())
    content = sheet.values.tolist()
    rows = []
    for j in range(len(content)):
        row = dict()
        # 如果有标记
        if has_status:
            if pd.isnull(content[j][-1]):
                row["status"] = 1
            else:
                row["status"] = int(content[j][-1])
            row["val"] = content[j][:-1]
        else:
            row["status"] = 1
            row["val"] = content[j]
        rows.append(row)


if __name__ == '__main__':
    test_file("/管理学院/2021/2021-7.xls")