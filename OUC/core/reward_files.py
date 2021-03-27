#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: qinchangshuai(cs_qin@qq.com) 
Date: 2021/1/16 10:32 
"""

import os

from OUC import log

logger = log.logger


def main():
    res = {"message": "success", "reward_files": []}
    tmp_reward_files = []
    try:
        files_name = os.listdir("OUC/static/reward_files/")
        for file_name in files_name:
            cur_dict = {}
            # 查看json文件中是否有自己的课程
            release_time, origin, name = file_name.split("_")
            cur_dict["release_time"] = release_time
            cur_dict["origin"] = origin
            cur_dict["name"] = name.split(".")[0]
            cur_dict["full_name"] = file_name
            tmp_reward_files.append(cur_dict)
        reward_files = sorted(tmp_reward_files, key=lambda x: x['release_time'], reverse=True)
        res["reward_files"] = reward_files
        return res
    except Exception as e:
        logger.error("%s获取奖励文件异常: %s" % (e))
        res["message"] = "fault"
        return res


if __name__ == '__main__':
    main()
