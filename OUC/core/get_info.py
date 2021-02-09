#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: qinchangshuai(cs_qin@qq.com) 
Date: 2021/2/8 21:54 
"""
from bs4 import BeautifulSoup
import base64
import time

from OUC.core.package import login
from OUC import log
from OUC import models
from OUC.global_config import headers

logger = log.logger


base_info_url = "http://pgs.ouc.edu.cn/gl/page/student/studentBaseOne.htm"
family_info_url = "http://pgs.ouc.edu.cn/gl/page/student/studentFamilyOne.htm"
source_info_url = "http://pgs.ouc.edu.cn/gl/page/student/studentSourceOne.htm"
student_info_url = "http://pgs.ouc.edu.cn/gl/page/student/studentException.htm"


class SpiderInfo(object):
    @classmethod
    def main(cls, sno, passwd, openid="null"):
        res = {"message": "", "info": ""}
        passwd = cls.base64decode(passwd)
        login_info = login.Login.login(sno, passwd, openid)
        if login_info["message"] == "success":
            session = login_info["session"]
            res["message"] = login_info["message"]
            try:
                base_info_page = session.get(base_info_url, headers=headers, timeout=6)
                base_info_soup = BeautifulSoup(base_info_page.text, 'lxml')
                # print(base_info_soup)
                tmp_base_info = base_info_soup.findAll(name="p", attrs={"class": "ml10 content w200 detail"})
                base_info = ["" for _ in range(len(tmp_base_info))]
                for i in range(len(tmp_base_info)):
                    base_info[i] = tmp_base_info[i].text.replace("\r", "").replace("\n", "").strip()
                base_info_dict = {
                    "sno": base_info[0],
                    "name": base_info[1],
                    "sex": base_info[4],
                    "date_of_birth": base_info[5],
                    "id_card": base_info[7],
                    "nation": base_info[8],
                    "id_info": base_info[10],
                    "hometown": base_info[14],
                    "start_year": base_info[15],
                    "study_period": base_info[16],
                    "degree_type": base_info[17],
                    "train_type": base_info[18],
                }

                # 家庭地址
                family_info_page = session.get(family_info_url, headers=headers, timeout=6)
                family_info_soup = BeautifulSoup(family_info_page.text, 'lxml')
                tmp_family_info = family_info_soup.findAll(name="p", attrs={"class": "ml10 content w500 detail"})
                family_info = ["" for _ in range(len(tmp_family_info))]
                for i in range(len(tmp_family_info)):
                    family_info[i] = tmp_family_info[i].text.replace("\r", "").replace("\n", "").strip()
                base_info_dict["hukou_address"] = family_info[0]
                base_info_dict["home_tel"] = family_info[1]
                base_info_dict["home_postcode"] = family_info[2]
                base_info_dict["home_detail"] = family_info[4]

                # 生源地
                source_info_page = session.get(source_info_url, headers=headers, timeout=6)
                source_info_soup = BeautifulSoup(source_info_page.text, 'lxml')
                tmp_source_info = source_info_soup.findAll(name="p", attrs={"class": "ml10 content w500 detail"})
                source_info = ["" for _ in range(len(tmp_source_info))]
                for i in range(len(tmp_source_info)):
                    source_info[i] = tmp_source_info[i].text.replace("\r", "").replace("\n", "").strip()
                base_info_dict["come_from"] = source_info[0]
                base_info_dict["file_unit"] = source_info[2]

                # 电话
                student_info_page = session.get(student_info_url, headers=headers, timeout=6)
                student_info_soup = BeautifulSoup(student_info_page.text, 'lxml')
                tmp_student_info = student_info_soup.findAll(name="p", attrs={"class": "right1"})
                student_info = ["" for _ in range(len(tmp_student_info))]
                for i in range(len(student_info)):
                    student_info[i] = tmp_student_info[i].text.replace("\r", "").replace("\n", "").strip()
                base_info_dict["tel"] = student_info[6]
                res["info"] = base_info_dict
                session.close()
                print(base_info_dict)
                return res
            except Exception as e:
                session.close()
                logger.error("[sno]: %s [passwd]: %s [Exception]: %s" % (sno, passwd, e))
                res['message'] = "fault"
                return res
        else:
            res["message"] = login_info["message"]
            return res

    @classmethod
    def travel_info(cls):
        try:
            # 找出符合学号年级的所有学生
            students = models.Student.objects.all()
            # 遍历列表开始时间
            travel_begin = time.time()
            for student in students:
                try:
                    cur_student = models.StudentInfo.objects.filter(sno=student.sno)
                    if len(cur_student) == 0:
                        spider_res = cls.main(student.sno, student.passwd)
                        if spider_res["message"] == "success":
                            info = spider_res["info"]
                            models.StudentInfo.objects.create(
                                sno=info["sno"],
                                name=info["name"],
                                sex=info["sex"],
                                date_of_birth=info["date_of_birth"],
                                id_card=info["id_card"],
                                nation=info["nation"],
                                id_info=info["id_info"],
                                hometown=info["hometown"],
                                start_year=info["start_year"],
                                study_period=info["study_period"],
                                degree_type=info["degree_type"],
                                train_type=info["train_type"],
                                hukou_address=info["hukou_address"],
                                home_tel=info["home_tel"],
                                home_postcode=info["home_postcode"],
                                home_detail=info["home_detail"],
                                come_from=info["come_from"],
                                file_unit=info["file_unit"],
                                tel=info["tel"],
                                department=student.department,
                                profession=student.profession,
                                research=student.research,
                                img_url="https://imgshenpi.ouc.edu.cn/avatarNew/%s.jpg" % student.sno
                            )
                            time.sleep(3)
                    else:
                        pass
                except Exception as e:
                    print(e)
            travel_end = time.time()
            logger.info("【信息获取】遍历%s个学生共耗时%ss" % (len(students), travel_end - travel_begin))
        except Exception as e:
            logger.error("【信息获取】获取学生失败！ %s" % e)

    @classmethod
    def base64decode(cls, passwd):
        """数据库密码解密"""
        decode_passwd = base64.b64decode(passwd.encode('GBK')).decode('ascii')  # .decode('ascii') 转换成字符形式
        return decode_passwd


if __name__ == '__main__':
    SpiderInfo.main("", "", "null")