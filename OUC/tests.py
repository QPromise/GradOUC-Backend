import time
import gevent
from gevent.pool import Pool
from gevent import monkey

monkey.patch_all()


class ABC(object):
    def __init__(self):
        # 一，限制最大并发数
        self.p = Pool(20)
        self.results = None
        self.num = 5
        # 二，导入gevent猴子补丁，没有它，协称就不会并发执行

    #  三，耗时任务或者阻塞任务，异步执行的或者需要并发的就是它了
    def task(self, i, num):
        print(i)
        time.sleep(i)

        self.num += 1
        self.results = self.num
        print("sum = {}".format(self.num))

    def run(self):
        time_l = time.time()
        # 四，任务派发，将15个任务派发给携程去做
        threads = [self.p.spawn(self.task, 2, self.num) for i in range(40)]

        # 五，在此阻塞，等所有协程全部完成退出，这一步才执行完
        gevent.joinall(threads)

        time_r = time.time()
        print("总耗时：{}".format(time_r - time_l))


if __name__ == "__main__":
    abc = ABC()
    abc.run()
    print(abc.results)