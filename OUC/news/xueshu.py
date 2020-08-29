"""
_*_coding:utf-8 _*_

@Time    :2019/11/11 11:03
@Author  :csqin 
@FileName: xuehsu.py
@Software: PyCharm

"""
# -*- coding: utf-8 -*-
import json
import html2text
import urllib.request
import math
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime

"""
网站新闻爬取
"""


def get_news(page):
    xuehsu_url = 'http://www.ouc.edu.cn/xshd/list' + str(page) + '.htm'
    # 第一层循环，把url都导出来
    # 定义发送的请求
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    req = urllib.request.Request(xuehsu_url, headers=head)
    # 将服务器返回的页面放入rsp变量
    rsp = urllib.request.urlopen(req)
    # 读取这个页面，并解码成utf-8格式，忽略错误,放入变量html中
    html = rsp.read().decode('utf-8', 'ignore')
    # 使用BeautifulSoup模块解析变量中的web内容
    news_soup = BeautifulSoup(html, 'html.parser')
    # publish_dates = html.select('.Article_PublishDate')
    # 获取隐藏字段
    temp_news = news_soup.find_all("span", {"class": "Article_Title"})
    temp_dates = news_soup.find_all("span", {"class": "Article_PublishDate"})
    # print(temp_news)
    total_news = []
    pages_count = int(news_soup.find("em", {"class": "all_pages"}).text)
    res = {"pages_count": "", "total_news": total_news}
    for elem_news, elem_date in zip(temp_news, temp_dates):
        news = {"id": "", "title": "", "date": ""}
        news["id"] = elem_news.find("a")["href"]
        news["title"] = str(elem_news.find("a")["title"]).strip()
        news["date"] = str(elem_date.text).strip()
        # print(elem_news.find("a"))
        # print(elem_date.text)
        total_news.append(news)
    # print(total_news)
    # print(pages_count)
    res["total_news"] = total_news
    res["pages_count"] = pages_count
    # eventId = news_soup.find("input", {"name": "_eventId"})
    return res


def get_newsDeatil(id):
    newsDetail_url = 'http://www.ouc.edu.cn' + str(id)
    # 第一层循环，把url都导出来
    # 定义发送的请求
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    req = urllib.request.Request(newsDetail_url, headers=head)
    # 将服务器返回的页面放入rsp变量
    rsp = urllib.request.urlopen(req)
    # 读取这个页面，并解码成utf-8格式，忽略错误,放入变量html中
    html = rsp.read().decode('utf-8', 'ignore')
    # 使用BeautifulSoup模块解析变量中的web内容
    news_soup = BeautifulSoup(html, 'lxml')
    # print(news_soup)
    title = news_soup.find("td", {"class": "atitle"}).text.strip()
    time = news_soup.find("span", {"class": "arti_update"}).text.strip()
    content = str(news_soup.find("div", {"class": "wp_articlecontent"}))
    image_url = re.findall(r'<img[^>]*src="([^"]*)"', content)
    if image_url != []:
        for url in image_url:
            if url.find('http') == -1:
                content = content.replace(url, 'http://www.ouc.edu.cn' + url)
    else:
        pass
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.bypass_tables = False
    text_maker.ignore_images = False
    res = {"title": title, "time": time, "content": text_maker.handle(str(content))}
    # print(res)
    return json.dumps(res)


if __name__ == '__main__':
    # get_news(1)
    get_newsDeatil('/2019/1031/c5739a274488/page.htm')
