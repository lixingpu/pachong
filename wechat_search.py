#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pyquery import PyQuery as pq
import time
import json
import re
import hashlib
import random
from pymongo import MongoClient

client = MongoClient('192.168.40.19',27017)
db = client.resultdb.weixin_zhongyi

#构造header头
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/538.1 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36')
driver = webdriver.PhantomJS("D:/phantomjs/bin/phantomjs.exe",desired_capabilities = dcap ,service_args=['--ignore-ssl-errors=true'])
driver.set_window_size(1366,768)

#添加cookie
with open("C:/cookies.txt") as f:
    cookies_list = json.loads(f.read())
driver.delete_all_cookies()
for cookie in cookies_list:
    try:
        driver.add_cookie(cookie)
    except:
        pass

#获取首页源码
def get_index_source(url):
    driver.get(url)
    time.sleep(4)
    html_src = driver.page_source
    html = html_src.replace("&amp;","&")
    return html

#获取源码中微信文章的url地址
def url_list(html):
    page_urllist = []
    pq_h = pq(html)
    for each in pq_h('a[uigs^="article_title"]').items():
        page_urllist.append(each.attr.href)
    return page_urllist

#计算md5值
def md5(ss):
    strmd5 =hashlib.md5()
    strmd5.update(ss.encode('utf-8'))
    return strmd5.hexdigest()

#解析微信文章的标题、发布时间、网页源码、图片列表,并且如果数据库中没有该文章则保存到数据库
def jiexi_wechat(url):
    driver.get(url)
    url_patten = re.compile(r'data-src=\"(.+?)\"')
    title = driver.title
    titlehash = md5(title)
    page_src = driver.page_source
    pq_h = pq(page_src)
    time = pq_h('#post-date').text()
    img_urls = url_patten.findall(page_src)

    sum = db.find({'titlehash':titlehash}).count()
    if sum == 0:
        result = {"url": url, "titlehash": titlehash, "title": title, "time": time, "img_urls": img_urls}
        db.insert(result)

#通过url page参数来访问某一页面
i = 1
while i < 14:

    url = 'http://weixin.sogou.com/weixin?oq=&query=%E4%B8%AD%E5%8C%BB&_sug_type_=1&sut=0&lkt=0%2C0%2C0&s_from=input&ri=0&_sug_=n&type=2&sst0=1516614623806&page=' + str(i) + '&ie=utf8&p=40040108&dp=1&w=01015002&dr=1'
    html = get_index_source(url)
    page_wz_url=url_list(html)
    for url in page_wz_url:
        jiexi_wechat(url)
    i = i + 1
    time.sleep(random.randint(10, 50))