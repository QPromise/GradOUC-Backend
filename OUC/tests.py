import time

cur = int(time.time())
end = 1610606871
print((end - cur) // (3600 * 24))

import requests
s = requests.session()
url = "https://www.baidu.com/"
s.keep_alive = False
s.proxies = {"http": "123.55.106.78:9999", "https": "123.55.102.199:9999", }
r = s.get(url)
print(r.status_code)  # 如果代理可用则正常访问，不可用报以上错误