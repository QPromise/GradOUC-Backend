#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: cs_qin(cs_qin@qq.com)
Date: 2020/8/30 22:06
"""

from bs4 import BeautifulSoup

from OUC.core.package import login
from OUC import log
from OUC.global_config import headers, profile_url

logger = log.logger


def main(sno, passwd, openid):
    res = {"message": "", "info": "", "have_class": 0}
    login_info = login.Login.login(sno, passwd, openid)
    if login_info["message"] == "success":
        session = login_info["session"]
        res["message"] = login_info["message"]
        try:
            profile_page = session.get(profile_url, headers=headers, timeout=6)
            session.close()
            profile_soup = BeautifulSoup(profile_page.text, 'lxml')
            name = profile_soup.findAll(name="dt", attrs={"class": "title cblue"})[0].text
            # ml10 content w300
            need_list = profile_soup.findAll(name="dd", attrs={"class": "ml10 content w300"})
            profession = need_list[2].text.split("：")[1]
            research = need_list[3].text.split("：")[1]
            supervisor = need_list[4].text.split("：")[1]
            info = {"name": name, "profession": profession, "research": research, "supervisor": supervisor}
            res["info"] = info
            res['have_info'] = 1
            return res
        except Exception as e:
            session.close()
            logger.error("[sno]: %s [passwd]: %s [Exception]: %s" % (sno, passwd, e))
            res['have_info'] = 2
            return res
    else:
        res["message"] = login_info["message"]
        res["have_info"] = 2
        return res


if __name__ == '__main__':
    print(main("21200231213", "", ""))
