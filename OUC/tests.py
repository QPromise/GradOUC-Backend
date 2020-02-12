from django.test import TestCase
import re
import datetime

string = "1-6dasdsa2-13dsad/.'l,"
print(re.findall(r"(\d+-\d+)",string))
# Create your tests here.
test = {"a":123,"b":456}
if "a" in test.keys():
    del test["a"]
    print(test)
else:
    print(123)

try:
    num = input(">>请输入数字")
    print("输入的数字为：{}".format(int(num)))
except ValueError:
    print(ValueError,"输入的不是数字")
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
