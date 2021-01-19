import time

cur = int(time.time())
end = 1610606871
print((end - cur) // (3600 * 24))

import requests
s = requests.session()
url = "https://www.baidu.com/"
s.keep_alive = False
s.proxies = {"http://1": "115.221.242.217:9999",
             "http://2": "36.250.156.145:9999",
             "http://3": "175.42.129.249:9999",
             "http://4": "123.55.98.191:9999",
             }
r = s.get(url)
print(r.status_code)  # 如果代理可用则正常访问，不可用报以上错误