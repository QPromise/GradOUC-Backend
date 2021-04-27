#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: qinchangshuai(cs_qin@qq.com) 
Date: 2021/4/27 15:22 
"""


from datetime import datetime

from OUC import log
from OUC import models

logger = log.logger


def get_news(page=1):
    res = {"message": "success", "news": []}
    try:
        news = models.DreamOUCNews.objects.all()
        if len(news) == 0:
            return res
        else:
            top_news = []
            general_news = []
            for news_ele in news:
                tmp_news_ele = dict()
                tmp_news_ele["id"] = news_ele.id
                tmp_news_ele["news_title"] = news_ele.news_title
                tmp_news_ele["news_url"] = news_ele.news_url
                tmp_news_ele["news_tag"] = process_news_tag(news_ele.news_tag)
                tmp_news_ele["news_is_top"] = news_ele.news_is_top
                tmp_news_ele["news_top_val"] = news_ele.news_top_val
                tmp_news_ele["published_time"] = datetime.strftime(news_ele.published_time, '%Y-%m-%d')
                tmp_news_ele["modified_time"] = datetime.strftime(news_ele.modified_time, '%Y-%m-%d')
                tmp_news_ele["news_attention"] = news_ele.news_attention
                if news_ele.news_is_top == 1:
                    top_news.append(tmp_news_ele)
                else:
                    general_news.append(tmp_news_ele)
            # 对置顶新闻排序
            if len(top_news) >= 1:
                top_news = sorted(top_news, key=lambda x: x['news_top_val'], reverse=True)
            res["news"] = top_news + general_news
            return res
    except Exception as e:
        logger.error("[DreamOUC Module][news.py] %s" % e)
        res["message"] = "fault"
        return res


def process_news_tag(tags):
    """
    拆分数据库中的用#分割的tag标签
    :param tags:
    :return:
    """
    if tags == "-":
        return []
    tags = tags.split("#")
    if len(tags) > 3:
        return tags[:3]
    return tags


def increase_news_attention(news_id):
    """
    增加文章阅读数
    :param news_id:
    :return:
    """
    res = {"message": "success", "news_attention": 0}
    try:
        news = models.DreamOUCNews.objects.filter(id=news_id).first()
        if news is not None:
            news.news_attention = news.news_attention + 1
            news.save()
            news_attention = models.DreamOUCNews.objects.filter(id=news_id).values("news_attention").first()['news_attention']
            res["news_attention"] = news_attention
            return res
        else:
            res["message"] = "empty"
            return res
    except Exception as e:
        logger.error("[DreamOUC Module][news.py][增加阅读数失败] %s" % e)
        res["message"] = "fault"
        return res
