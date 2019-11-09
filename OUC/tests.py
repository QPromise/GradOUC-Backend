from django.test import TestCase
import re
string = "1-6dasdsa2-13dsad/.'l,"
print(re.findall(r"(\d+-\d+)",string))
# Create your tests here.
test = {"a":123,"b":456}
if "a" in test.keys():
    del test["a"]
    print(test)
else:
    print(123)

