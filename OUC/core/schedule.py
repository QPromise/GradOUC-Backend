#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: cs_qin(cs_qin@qq.com)
Date: 2020/8/30 22:06
"""

import pandas as pd
import numpy as np
import re

from OUC.core.package import login

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}

# 课表地址
schedule_url = "http://pgs.ouc.edu.cn/py/page/student/grkcb.htm"


def main(sno, passwd, openid, zc, xj, xn):
    res = {"message": "", "schedule": ""}
    login_info = login.Login.login(sno, passwd, openid)
    if login_info["message"] == "success":
        session = login_info["session"]
        res["message"] = login_info["message"]
        try:
            param = "?zc=" + str(zc) + "&xj=" + str(xj) + "&xn=" + str(xn)
            schedule_page = session.get(url=schedule_url + param, headers=headers)
            # 我的课程表
            decided_table = pd.read_html(schedule_page.text)[0]
            # 课程表
            decided_table = [decided_table['星期一'].values, decided_table['星期二'].values,
                             decided_table['星期三'].values,
                             decided_table['星期四'].values, decided_table['星期五'].values,
                             decided_table['星期六'].values, decided_table['星期日'].values]
            decided_table = pd.DataFrame(decided_table).fillna('')
            # print(decided_table)
            decided_table = np.array(decided_table)
            schedule = []
            for i in range(12):
                row = []
                temp = decided_table[:, i].tolist()
                # print(temp)
                for j in range(7):
                    now_class = {"name": "", "room": "", "leader": "", "color": "", "index": "", "time": "",
                                 "period": ""}
                    # 当前没有课的话
                    if temp[j] == '':
                        row.append(now_class)
                        continue
                    else:
                        # 拆分课程信息
                        class_info = temp[j].split()
                        now_class["period"] = re.findall(r"(\d+-\d+)", decided_table[:, i][j])[0]
                        now_class["name"] = class_info[0]
                        now_class["room"] = class_info[-1]
                        now_class["leader"] = class_info[-2]
                        row.append(now_class)
                schedule.append(row)
            res['schedule'] = schedule
            return res
        except Exception as e:
            return res
    else:
        res["message"] = login_info["message"]
        return res

# """
# 以下课程时间地点待定,具体请关注课程备注或相关通知：
# """
# undetermined_table = pd.read_html(schedule_page.text)[1]
# undetermined_schedule = pd.DataFrame(undetermined_table)
# undetermined_schedule = undetermined_schedule.fillna('no_info')
# print(undetermined_schedule)
# undetermined_schedule.to_csv(r'store.csv', mode='a', encoding='utf_8_sig')


if __name__ == '__main__':
    main("21190211105", "", "", "1", "12", "2019")
