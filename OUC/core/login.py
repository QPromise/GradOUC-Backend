"""
_*_coding:utf-8 _*_

@Time    :2019/11/3 14:22
@Author  :csqin
@FileName: login.py
@Software: PyCharm

"""
import base64
import requests
import pandas as pd
from bs4 import BeautifulSoup
from requests import RequestException
headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}

# 登录地址
login_url = "http://id.ouc.edu.cn:8071/sso/login?service=http%3A%2F%2Fpgs.ouc.edu.cn%2Fallogene%2Fpage%2Fhome.htm%3B"
new_login_url = "http://pgs.ouc.edu.cn/sso/login?service=http%3A%2F%2Fpgs.ouc.edu.cn%2Fpy%2Fpage%2Fstudent%2Fxslcsm.htm%3B"
# 登录后的主页
home_url = "http://pgs.ouc.edu.cn/allogene/page/home.htm;"


def base64encode(passwd):
    encode_passwd = base64.b64encode(passwd.encode('GBK'))  # .decode('ascii') 转换成字符形式
    return encode_passwd

def main(username = '',password = ''):
    # 创建一个回话
    session = requests.Session()

    # 获得登录页面
    response = session.get(login_url)
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

    res = {"message": "", "name": ""}
    try:
        # 提交登录表单
        post_form = session.post(url=login_url, headers=headers, data=values)
        # 获取登录后主页面
        res["message"] = "timeout"
        home_page = session.get(url=home_url, headers=headers,timeout=6)
        res["message"] = "fault"
        home_soup = BeautifulSoup(home_page.text, 'lxml')
        if home_soup.findAll(name="div", attrs={"class": "panel_password"}):
            print('登录失败!')
            return res
        else:
            print('登录成功!')
            res["message"] = "success"
            self_info = pd.read_html(home_page.text)[0]
            print(pd.DataFrame(self_info))
            name = pd.DataFrame(self_info)[1][0]
            res["name"] = name
            return res
    except Exception as e:
        print(e)
        return res

if __name__ == '__main__':
    main("21180231272","")


