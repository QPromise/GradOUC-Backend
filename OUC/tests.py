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

# 构造一个将来的时间
future = datetime.strptime('2019-12-22 00:00:00', '%Y-%m-%d %H:%M:%S')
# 当前时间
now = datetime.now()
print(now)
# 求时间差
delta = future - now
print(delta)
hour = delta.seconds / 60 / 60
minute = (delta.seconds - hour * 60 * 60) / 60
seconds = delta.seconds - hour * 60 * 60 - minute * 60
print_now = now.strftime('%Y-%m-%d %H:%M:%S')