#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from selenium import webdriver
import os
import time
import json
import random
from pyquery import PyQuery as pq

post={}
print("启动浏览器，打开微信公众号登录界面")
driver = webdriver.Chrome()
# 打开微信公众号登录页面
driver.get('http://weixin.sogou.com/')
# 等待5秒钟
time.sleep(5)

driver.find_element_by_id("loginBtn").click()
# 拿手机扫二维码！
print("请拿手机扫码二维码登录公众号")
time.sleep(10)
print("登录成功")
# 重新载入公众号登录页，登录之后会显示公众号后台首页，从这个返回内容中获取cookies信息
driver.get('http://weixin.sogou.com/')
time.sleep(1)
driver.find_element_by_id("query").send_keys('中医')
time.sleep(1)
driver.find_element_by_class_name("swz").click()
time.sleep(1)

post = {}
cookie_items = driver.get_cookies()
for cookie_item in cookie_items:
    post[cookie_item['name']] = cookie_item['value']
cookie_str = json.dumps(post)
with open('C:\cookies.txt', 'w+', encoding='utf-8') as f:
    f.write(cookie_str)

print (cookie_items)