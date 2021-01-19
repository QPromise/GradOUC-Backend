#!/usr/bin/python3
# _*_coding:utf-8 _*_

"""
Author: cs_qin(cs_qin@qq.com)
Date: 2020/8/30 22:06
"""

import json
import html2text
import urllib.request
from bs4 import BeautifulSoup
import re
import time

from OUC import log
from OUC.core.package import login

logger = log.logger

"""
网站新闻爬取
"""


def get_news(page):
    yanzhao_url = 'http://yz.ouc.edu.cn/5926/list' + str(page) + '.htm'
    # 第一层循环，把url都导出来
    # 定义发送的请求
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    proxy_support = urllib.request.ProxyHandler(login.ProxyIP.get_ip())
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    req = urllib.request.Request(yanzhao_url, headers=head)
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
        news = dict()
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
    try:
        newsDetail_url = 'http://yz.ouc.edu.cn' + str(id)
        # 第一层循环，把url都导出来
        # 定义发送的请求
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        proxy_support = urllib.request.ProxyHandler(login.ProxyIP.get_ip())
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        req = urllib.request.Request(newsDetail_url, headers=head)
        # 将服务器返回的页面放入rsp变量
        rsp = urllib.request.urlopen(req)
        # 读取这个页面，并解码成utf-8格式，忽略错误,放入变量html中
        html = rsp.read().decode('utf-8', 'ignore')
        # 使用BeautifulSoup模块解析变量中的web内容
        news_soup = BeautifulSoup(html, 'lxml')
        # print(news_soup)
        try:
            title = news_soup.find("h1", {"class": "arti_title"}).text.strip()
            news_time = news_soup.find("span", {"class": "arti_update"}).text.strip()
            content = str(news_soup.find("div", {"class": "wp_articlecontent"}))
            image_url = re.findall(r'<img[^>]*src="([^"]*)"', content)
            link_url = re.findall(r'<a[^>]*href="([^"]*)"', content)
            pdf_url = re.findall(r'<div[^>]*pdfsrc="([^"]*)"', content)
            # print(pdf_url)
            pdf_div = re.findall(r'<div[^>]*pdfsrc=.*"></div>', content)
            # print(image_url)
            # print(link_url)
            # print(pdf_div)  # class="wp_pdf_player"
            # 如果页面中有图片链接 则替换为相对路径
            if len(image_url) != 0:
                for url in image_url:
                    if content.find("icon_doc") == -1 and content.find("icon_xls") == -1:
                        content = content.replace(url, 'http://yz.ouc.edu.cn' + url)
                    else:
                        content = content.replace(url, "")
            else:
                pass
            # 如果页面中有地址链接 则替换为相对路径
            if len(link_url) != 0:
                for url in link_url:
                    if url.find('http') == -1:
                        content = content.replace(url, 'http://yz.ouc.edu.cn' + url)
                    else:
                        pass
            else:
                pass
            # pdf路径替换
            if len(pdf_div) != 0:
                for i, pdf in enumerate(pdf_div):
                    if pdf.find('http') == -1:
                        pdf_url = re.findall(r'<div[^>]*pdfsrc="([^"]*)"', pdf)
                        if pdf_url != []:
                            content = content.replace(pdf, '<a href = "http://yz.ouc.edu.cn' + pdf_url[0] + '">附件' + str(
                                i + 1) + '地址，点击复制去浏览器下载</a>')

                        else:
                            pass
                    else:
                        pass
            else:
                pass
            # print(content)
            text_maker = html2text.HTML2Text()
            text_maker.bypass_tables = True
            text_maker.ignore_images = False
            res = {"title": title, "time": news_time, "content": text_maker.handle(content), "news_url": newsDetail_url}
        except Exception as e:
            logger.error("[yanzhao][newsDetail_url]: %s[Exception]: %s" % (newsDetail_url, e))
            res = {"title": "访问出现错误", "time": "访问时间：" + time.strftime("%Y-%m-%d %H:%M", time.localtime()),
                   "content": "内容无法显示，请复制网址去浏览器查看", "news_url": newsDetail_url}
        # print(res)
        return json.dumps(res)
    except Exception as e:
        logger.error("[yanzhao][newsDetail_url]: %s [Exception]: %s" % (newsDetail_url, e))
        res = {"title": "访问失败", "time": "访问时间：" + time.strftime("%Y-%m-%d %H:%M", time.localtime()),
               "content": "查看该内容需要权限，请复制网址去浏览器查看", "news_url": newsDetail_url}
        return json.dumps(res)


if __name__ == '__main__':
    # get_news(2)
    get_newsDeatil('/2019/1110/c5926a275557/page.htm')
