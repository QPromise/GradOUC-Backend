import time
import bs4
from bs4 import  BeautifulSoup
cur = int(time.time())
end = 1610606871
print((end - cur) // (3600 * 24))
expire_time = time.strptime("2021-01-20 15:32:08", "%Y-%m-%d %H:%M:%S")
expire_time = int(time.mktime(expire_time))
print(2020 in range(2020, 2020))
print(",".join(list(map(str, ["计算机科学"]))))
print("http://grad.ouc.edu.cn/"[:-1])
# print(begin_day)
#
# import requests
# s = requests.session()
# headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
#         'Connection': 'close'
#     }
# url = "http://www.baidu.com/"
# s.keep_alive = False
# s.proxies = {
#                 "http": "182.34.27.148:9999"
#              }
# r = s.get(url, headers=headers)
# profile_soup = BeautifulSoup(r.text, 'lxml')
# print(profile_soup)
# print(r.status_code)  # 如果代理可用则正常访问，不可用报以上错误