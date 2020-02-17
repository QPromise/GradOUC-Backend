"""
_*_coding:utf-8 _*_

@Time    :2019/11/3 14:50
@Author  :csqin 
@FileName: schedule.py
@Software: PyCharm

"""
import base64
import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import re
headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}

# 登录地址
login_url = "http://id.ouc.edu.cn:8071/sso/login?service=http%3A%2F%2Fpgs.ouc.edu.cn%2Fallogene%2Fpage%2Fhome.htm%3B"
new_login_url = "http://pgs.ouc.edu.cn/sso/login?service=http%3A%2F%2Fpgs.ouc.edu.cn%2Fpy%2Fpage%2Fstudent%2Fxslcsm.htm%3B"
# 登录后主页
home_url = "http://pgs.ouc.edu.cn/allogene/page/home.htm;"
# 课表地址
schedule_url = "http://pgs.ouc.edu.cn/py/page/student/grkcb.htm;"

def base64encode(passwd):
    encode_passwd = base64.b64encode(passwd.encode('GBK'))  # .decode('ascii') 转换成字符形式
    return encode_passwd


def main(username = '',password = '',zc = '',xj = '',xn = ''):
    # 创建一个回话
    session = requests.Session()

    # 获得登录页面
    response = session.get(new_login_url)
    login_soup = BeautifulSoup(response.text, 'lxml')

    # 获取隐藏字段
    lt = login_soup.form.find("input", {"name": "lt"})["value"]
    eventId = login_soup.form.find("input", {"name": "_eventId"})["value"]

    # 填写post信息
    values = {
        "username": username,
        "password": base64encode(password),
        "lt": lt,
        "_eventId": eventId
    }

    res = {"message": "", "schedule": ""}
    try:
        # 提交登录表单
        post_form = session.post(url=new_login_url, headers=headers, data=values)
        # 获取登录后主页面
        res['message'] = 'timeout'
        home_page = session.get(url=home_url, headers=headers,timeout = 6)
        res['message'] = 'fault'
        home_soup = BeautifulSoup(home_page.text, 'lxml')
        param = "?zc="+str(zc)+"&xj="+str(xj)+"&xn="+str(xn)
        if home_soup.findAll(name="div", attrs={"class": "panel_password"}):
            print('登录失败!')
            return res
        else:
            print('登录成功!')
            res["message"] = "success"
            self_info = pd.read_html(home_page.text)[0]
            print(pd.DataFrame(self_info))
            name = pd.DataFrame(self_info)[1][0]
            schedule_page = session.get(url=schedule_url + param, headers=headers)
            """
            我的课程表
            """
            decided_table = pd.read_html(schedule_page.text)[0]
            # 课程表
            decided_table = [decided_table['星期一'].values,  decided_table['星期二'].values,
                              decided_table['星期三'].values,
                             decided_table['星期四'].values, decided_table['星期五'].values,
                             decided_table['星期六'].values, decided_table['星期日'].values]
            decided_table = pd.DataFrame(decided_table).fillna('')
            decided_table = np.array(decided_table)
            schedule = []
            for i in range(12):
                row = []
                temp = decided_table[:, i].tolist()
                for j in range(7):
                    now_class = {"name":"","room":"","leader":"","color":"","index":"","time":"","period":""}
                    # 当前没有课的话
                    if temp[j] == '':
                        row.append(now_class)
                        continue
                    else:
                        # 拆分课程信息
                        class_info = temp[j].split()
                        # print(class_info)
                        now_class["period"] = re.findall(r"(\d+-\d+)", decided_table[:, i][j])[0]
                        now_class["name"] = class_info[0]
                        now_class["room"] = class_info[-1]
                        now_class["leader"] = class_info[-2]
                        row.append(now_class)
                schedule.append(row)
            for i in range(len(schedule)):
                print(schedule[i])
            res['schedule'] = schedule
            return res
    except Exception as e:
        print(e)
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
    main("21190211105","","12","11","2019")
    # "21190211105",""