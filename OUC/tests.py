import time
import bs4
from bs4 import  BeautifulSoup
cur = int(time.time())
end = 1610606871
print((end - cur) // (3600 * 24))

import requests
s = requests.session()
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        'Connection': 'close'
    }
url = "http://www.baidu.com/"
s.keep_alive = False
s.proxies = {
                "http": "182.34.27.148:9999"
             }
r = s.get(url, headers=headers)
profile_soup = BeautifulSoup(r.text, 'lxml')
print(profile_soup)
print(r.status_code)  # 如果代理可用则正常访问，不可用报以上错误