from django.test import TestCase
import re
import datetime
import requests
from bs4 import BeautifulSoup
import numpy as np
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}
score_url = "https://yz.chsi.com.cn/apply/cjcx/cjcx.do"
def main(xm = "王洁",zjhm = "370784199711107825",ksbh = "104230370709160",bkdwdm = "10423"):
    data = {
            "xm": xm,
            "zjhm": zjhm,
            "ksbh": ksbh,
            "bkdwdm": bkdwdm,
            "checkcode":""
        }
    session = requests.Session()
    score_page = session.post(url=score_url, headers=headers, data=data)
    score_soup = BeautifulSoup(score_page.text, 'lxml')
    # print(score_soup)
    try:
        if score_soup.findAll(name="div", attrs={"class": "zx-no-answer"}):
            res = score_soup.find("div", {"class": "zx-no-answer"}).text.strip()
            print("{0}----{1}".format(datetime.time,res))
    except Exception as e :
        print(e)
        print(score_soup)


if __name__ == '__main__':
    main()
"""
xm: 王洁
zjhm: 370784199711107825
ksbh: 104230370709160
bkdwdm: 10423
checkcode: 
"""
# string = "1-6dasdsa2-13dsad/.'l,"
# print(re.findall(r"(\d+-\d+)",string))
# # Create your tests here.
# test = {"a":123,"b":456}
# if "a" in test.keys():
#     del test["a"]
#     print(test)
# else:
#     print(123)
#
# try:
#     num = input(">>请输入数字")
#     print("输入的数字为：{}".format(int(num)))
# except ValueError:
#     print(ValueError,"输入的不是数字")
# print(eval(input('input m = ')+'**2'))
#
#
#
# import  requests
# from bs4 import BeautifulSoup
# url='https://support.microsoft.com/zh-cn/help/4519972'
# response = requests.get(url)
# print(response.text)
# soup = BeautifulSoup(response.text, 'lxml')
# # print(soup)
# res = soup.find("div", {"class": "content-article"})
# print('res = ',res)
