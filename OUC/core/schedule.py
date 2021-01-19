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
from OUC import log

logger = log.logger

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Connection': 'close'
}

# 课表地址
schedule_url = "http://pgs.ouc.edu.cn/py/page/student/grkcb.htm"


def main(sno, passwd, openid, zc, xj, xn):
    res = {"message": "", "schedule": [{"name": "", "room": "", "leader": "", "color": "", "index": "", "time": "",
                                 "period": ""}]}
    login_info = login.Login.login(sno, passwd, openid)
    if login_info["message"] == "success":
        session = login_info["session"]
        res["message"] = login_info["message"]
        try:
            param = "?zc=" + str(zc) + "&xj=" + str(xj) + "&xn=" + str(xn)
            schedule_page = session.get(url=schedule_url + param, headers=headers, timeout=6)
            session.close()
            # print(schedule_page.text)
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
                        period_re = re.compile(r'[(](.*?)[)]', re.S)
                        # print(decided_table[:, i][j])
                        # print(re.findall(period_re, decided_table[:, i][j])[0])
                        tmp_period = re.findall(period_re, decided_table[:, i][j])
                        if len(tmp_period) == 0:
                            period = "未知"
                        else:
                            period = tmp_period[0]
                        now_class["period"] = period
                        # now_class["period"] = re.findall(r"(\d+-\d+)", decided_table[:, i][j])[0]
                        now_class["name"] = class_info[0]
                        now_class["room"] = class_info[-1]
                        now_class["leader"] = class_info[-2]
                        row.append(now_class)
                schedule.append(row)
            res['schedule'] = schedule
            return res
        except Exception as e:
            session.close()
            logger.error("[sno]: %s [passwd]: %s [Exception]: %s" % (sno, passwd, e))
            res["message"] = "timeout"
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
    # main("", "", "null", "17", "11", "2020")
    main("21180231272", "", "null", "17", "11", "2020")
