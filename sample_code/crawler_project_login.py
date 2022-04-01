from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import pandas as pd
import os
import time
import re
import datetime
import threading
import json


def crawler_project_ali():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=8000,7000")
    chrome_options.add_argument('disable-javascrip')
    prefs = {'download.default_directory' : '/Users/michael/Downloads/ali'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome("chromedriver", 0, options=chrome_options)
    driver.get('http://www.ebiaoxun.com/search?keywords=')
    cookie_path = '/Users/michael/project/cookie.txt'
    #time.sleep(10)#等待扫码时间
    with open(cookie_path, 'r', encoding='utf-8') as f:
        cookies = f.readlines() 
    for cookie in cookies:
        cookie=cookie.replace(r'\n', '')
        cookie_li = json.loads(cookie)
        time.sleep(3)
    for cookie in cookie_li:
        driver.add_cookie(cookie)
        driver.refresh()
    driver.find_element_by_xpath('//i[@class="iconfont sou"]').click()
    driver.find_element_by_xpath('//input[@value="中标企业搜索"]').click()
    driver.find_element_by_xpath('//input[@class="searchname"]').send_keys('阿里云计算有限公司')
    driver.implicitly_wait(5)
    driver.find_element_by_xpath('//input[@class="中标企业搜索"]').send_keys('阿里云计算有限公司')

if __name__ == '__main__':
    #    for t in threads:
#        t.start()
    crawler_project_ali()
