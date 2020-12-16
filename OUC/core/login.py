#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: cs_qin(cs_qin@qq.com)
Date: 2020/8/30 22:06
"""

import pandas as pd
from bs4 import BeautifulSoup

from OUC.core.package import login

headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}

# 登录后的主页
home_url = "http://pgs.ouc.edu.cn/allogene/page/home.htm"
# profile
profile_url = "http://pgs.ouc.edu.cn/py/page/student/ckgrxxjh.htm"


def main(username, password):
    res = {"message": "", "name": ""}
    login_info = login.Login.login(username, password)
    if login_info["message"] == "success":
        session = login_info["session"]
        res["message"] = login_info["message"]
        try:
            home_page = session.get(url=home_url, headers=headers, timeout=6)
            self_info = pd.read_html(home_page.text)[0]
            name = pd.DataFrame(self_info)[1][0]
            res["name"] = name
            return res
        except Exception as e:
            print(e)
            try:
                profile_page = session.get(profile_url, headers=headers)
                profile_soup = BeautifulSoup(profile_page.text, 'lxml')
                name = profile_soup.findAll(name="dt", attrs={"class": "title cblue"})[0].text
                res["name"] = name
                return res
            except Exception as e:
                print(e)
                res["message"] = "timeout"
                return res
    else:
        res["message"] = login_info["message"]
        return res


if __name__ == '__main__':
    main("21180231272", "")
