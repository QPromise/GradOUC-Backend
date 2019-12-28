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



import  requests
from bs4 import BeautifulSoup
url='https://support.microsoft.com/zh-cn/help/4519972'
response = requests.get(url)
print(response.text)
soup = BeautifulSoup(response.text, 'lxml')
# print(soup)
res = soup.find("div", {"class": "content-article"})
print('res = ',res)
