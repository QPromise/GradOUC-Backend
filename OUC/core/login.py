#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: cs_qin(cs_qin@qq.com)
Date: 2020/8/30 22:06
"""

import pandas as pd
from bs4 import BeautifulSoup

from OUC.core.package import login
from OUC import log
from OUC.global_config import headers, home_url, profile_url

logger = log.logger


def main(sno, passwd, openid):
    res = {"message": "", "name": ""}
    login_info = login.Login.login(sno, passwd, openid)
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
            logger.error("[sno]: %s [passwd]: %s [Exception]: %s" % (sno, passwd, e))
            try:
                profile_page = session.get(profile_url, headers=headers, timeout=6)
                session.close()
                profile_soup = BeautifulSoup(profile_page.text, 'lxml')
                name = profile_soup.findAll(name="dt", attrs={"class": "title cblue"})[0].text
                res["name"] = name
                return res
            except Exception as e:
                session.close()
                logger.error("[sno]: %s [passwd]: %s [Exception]: %s" % (sno, passwd, e))
                res["message"] = "timeout"
                return res
    else:
        res["message"] = login_info["message"]
        return res


if __name__ == '__main__':
    main("", "", "11111")
