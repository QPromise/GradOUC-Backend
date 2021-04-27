#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: qinchangshuai(cs_qin@qq.com) 
Date: 2021/4/26 18:50 
"""

from OUC import log
from OUC import models

logger = log.logger


def get_cur_profession_material(profession_name):
    res = {"message": "success", "profession_material_info": {}}
    try:
        profession_material_info = models.DreamOUCProfession.objects.filter(profession_name=profession_name).first()
        if profession_material_info is not None:
            profession_material_info.profession_hot_val = profession_material_info.profession_hot_val + 1
            profession_material_info.save()
            res["profession_material_info"]["profession_hot_val"] = profession_material_info.profession_hot_val
            res["profession_material_info"]["profession_material_title"] = profession_material_info.profession_material_title
            res["profession_material_info"]["profession_material_url"] = profession_material_info.profession_material_url
            res["profession_material_info"]["open_course_title"] = profession_material_info.open_course_title
            res["profession_material_info"]["open_course_url"] = profession_material_info.open_course_url
            res["profession_material_info"]["taobao_key"] = profession_material_info.taobao_key
            res["profession_material_info"]["update_intro"] = profession_material_info.update_intro
            res["profession_material_info"]["profession_material_description"] = profession_material_info.profession_material_description
            return res
        else:
            res["message"] = "empty"
            return res
    except Exception as e:
        logger.error("[DreamOUC Module][profession_material.py] %s" % e)
        res["message"] = "fault"
        return res
