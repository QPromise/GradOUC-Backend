str = '\xe9\xaa\xa8\xe7\xb2\xbe\xe7\x81\xb5\xe7\x9a\x84\xe5\xb0\x8f\xe5\x8f\xaf\xe7\x88\xb1'
res = str.encode('raw_unicode_escape').decode('utf-8')
print(res)
import time
import datetime
print( time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()))