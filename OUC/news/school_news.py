#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: qinchangshuai(cs_qin@qq.com) 
Date: 2021/1/28 10:13 
"""
import json
import html2text
import urllib.request
from bs4 import BeautifulSoup
import re
import time

from OUC import log
from OUC.core.package import proxy

logger = log.logger


class SchoolNews(object):
    # 1001 代表研招网 1002 代表学术资讯 1003 代表后勤公告 1004 代表学校新闻 1005 代表研究生院新闻
    news_url = {
        "1001": "http://yz.ouc.edu.cn/5926/list%s.htm",
        "1002": "http://www.ouc.edu.cn/xshd/list%s.htm",
        "1003": "http://hqbzc.ouc.edu.cn/1670/list%s.htm",
        "1004": "http://www.ouc.edu.cn/xsdt/list%s.htm",
        "1005": "http://grad.ouc.edu.cn/13024/list%s.htm"
    }
    news_detail_url = {
        "1001": "http://yz.ouc.edu.cn",
        "1002": "http://www.ouc.edu.cn",
        "1003": "http://hqbzc.ouc.edu.cn",
        "1004": "http://www.ouc.edu.cn",
        "1005": "http://grad.ouc.edu.cn/"
    }

    def __init__(self):
        pass

    @classmethod
    def get_news(cls, news_type, page):
        proxy_support = urllib.request.ProxyHandler(proxy.ProxyIP.get_ip())
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        url = cls.news_url[news_type] % page
        rsp = urllib.request.urlopen(url)
        # 读取这个页面，并解码成utf-8格式，忽略错误,放入变量html中
        html = rsp.read().decode('utf-8', 'ignore')
        # 使用BeautifulSoup模块解析变量中的web内容
        news_soup = BeautifulSoup(html, 'html.parser')
        # 获取隐藏字段
        if news_type == "1003":
            temp_news = news_soup.find_all("span", {"class": "news_title"})
            temp_dates = news_soup.find_all("span", {"class": "news_meta"})
        else:
            temp_news = news_soup.find_all("span", {"class": "Article_Title"})
            temp_dates = news_soup.find_all("span", {"class": "Article_PublishDate"})
        total_news = []
        pages_count = int(news_soup.find("em", {"class": "all_pages"}).text)
        res = {"pages_count": "", "total_news": total_news}
        for elem_news, elem_date in zip(temp_news, temp_dates):
            news = dict()
            news["id"] = elem_news.find("a")["href"]
            if news["id"] == '/_redirect?siteId=372&columnId=14786&articleId=307032':
                continue
            news["title"] = str(elem_news.find("a")["title"]).strip()
            news["date"] = str(elem_date.text).strip()
            total_news.append(news)
        res["total_news"] = total_news
        res["pages_count"] = pages_count
        return res

    @classmethod
    def get_news_detail(cls, news_type, news_id):
        news_detail_url = cls.news_detail_url[news_type] + news_id
        replace_url = cls.news_detail_url[news_type]
        if news_type == "1005":
            replace_url = replace_url[:-1]
        try:
            # 第一层循环，把url都导出来
            # req = urllib.request.Request(newsDetail_url, headers=head)
            # 将服务器返回的页面放入rsp变量
            proxy_support = urllib.request.ProxyHandler(proxy.ProxyIP.get_ip())
            opener = urllib.request.build_opener(proxy_support)
            urllib.request.install_opener(opener)
            rsp = urllib.request.urlopen(news_detail_url)
            # 读取这个页面，并解码成utf-8格式，忽略错误,放入变量html中
            html = rsp.read().decode('utf-8', 'ignore')
            # 使用BeautifulSoup模块解析变量中的web内容
            news_soup = BeautifulSoup(html, 'lxml')
            try:
                if news_type in ["1001", "1003", "1005"]:
                    title = news_soup.find("h1", {"class": "arti_title"}).text.strip()
                else:
                    title = news_soup.find("td", {"class": "atitle"}).text.strip()
                news_time = news_soup.find("span", {"class": "arti_update"}).text.strip()
                content = str(news_soup.find("div", {"class": "wp_articlecontent"}))
                image_url = re.findall(r'<img[^>]*src="([^"]*)"', content)
                link_url = re.findall(r'<a[^>]*href="([^"]*)"', content)
                pdf_url = re.findall(r'<div[^>]*pdfsrc="([^"]*)"', content)
                pdf_div = re.findall(r'<div[^>]*pdfsrc=.*"></div>', content)
                if news_type in ["1001", "1003", "1004", "1005"]:
                    # 如果页面中有图片链接 则替换为相对路径
                    if len(image_url) != 0:
                        for url in image_url:
                            if content.find("icon_doc") == -1 and content.find("icon_xls") == -1:
                                content = content.replace(url, replace_url + url)
                            else:
                                content = content.replace(url, "")
                    # 如果页面中有地址链接 则替换为相对路径
                    if len(link_url) != 0:
                        for url in link_url:
                            if url.find('http') == -1:
                                content = content.replace(url, replace_url + url)
                    # pdf路径替换
                    if len(pdf_div) != 0:
                        for i, pdf in enumerate(pdf_div):
                            if pdf.find('http') == -1:
                                pdf_url = re.findall(r'<div[^>]*pdfsrc="([^"]*)"', pdf)
                                if pdf_url != []:
                                    content = content.replace(pdf, '<a href = "' + replace_url + pdf_url[0] + '">附件' + str(i + 1) + '地址，点击复制去浏览器下载</a>')
                    text_maker = html2text.HTML2Text()
                    text_maker.bypass_tables = True
                    text_maker.ignore_images = False
                elif news_type in ["1002"]:
                    if len(image_url) != 0:
                        for url in image_url:
                            if url.find('http') == -1:
                                content = content.replace(url, replace_url + url)
                    text_maker = html2text.HTML2Text()
                    text_maker.ignore_links = True
                    text_maker.bypass_tables = False
                    text_maker.ignore_images = False
                res = {"title": title, "time": news_time, "content": text_maker.handle(content), "news_url": news_detail_url}
            except Exception as e:
                logger.error("[houqin][newsDetail_url]: %s [Exception]: %s" % (news_detail_url, e))
                res = {"title": "访问失败", "time": "访问时间：" + time.strftime("%Y-%m-%d %H:%M", time.localtime()),
                       "content": "内容无法显示，请复制网址去浏览器查看", "news_url": news_detail_url}
            return json.dumps(res)
        except Exception as e:
            logger.error("[houqin][newsDetail_url]: %s [Exception]: %s" % (news_detail_url, e))
            res = {"title": "访问失败", "time": "访问时间：" + time.strftime("%Y-%m-%d %H:%M", time.localtime()),
                   "content": "查看该内容需要权限，请复制网址去浏览器查看", "news_url": news_detail_url}
            return json.dumps(res)
