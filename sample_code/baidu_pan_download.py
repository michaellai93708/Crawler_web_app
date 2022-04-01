from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import os
import time
import re
import datetime
import json


input_ = '链接: https://pan.baidu.com/s/1kqBm_nzk23K9xiCpP7pEwg 提取码: 7rd7 '


if re.findall('：', input_):
    chn_sign = re.findall('：', input_)
    for i in chn_sign:
        input_ = input_.replace('：', ': ')
else:
    input_ = input_
print(input_)
texts = input_.split()
#print(input_)
#print(texts)
for text in texts:
    if re.search('https://pan.baidu.+', text):
        url_object = re.search('https://pan.baidu.+', text)
        url = url_object.group(0)
        #print(url)
    else:
        message = '找不到合法链接'
if re.findall(r'提取码: .*',input_):
    password = re.findall(r'提取码: .*',input_)
    pass_ = password[0].split()
    password = pass_[1]
    #print(password)
else:
    password = None

print (url, password)
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=8000,7000")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('disable-javascrip')
prefs = {'download.default_directory' : '/Users/michael/Downloads'}
chrome_options.add_experimental_option('prefs', prefs)
cookie_path = '/Users/michael/Desktop/Work/Often_used_py_File/cookie.txt'
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
#print

if password:
    try:
        driver.find_element_by_xpath('//input[@id="accessCode"]').send_keys(password)
        driver.find_element_by_xpath('//span[@class="g-button-right"]').click()
        time.sleep(1)
    except:
        print('链接过期')
        driver.quit()
        #return
else:
    pass

with open(cookie_path, 'r', encoding='utf-8') as f:
    cookies = f.readlines() 
for cookie in cookies:
    cookie=cookie.replace(r'\n', '')
    cookie_li = json.loads(cookie)
    #time.sleep(3)
    #for cookie in cookie_li:   
driver.add_cookie(cookie_li[0])
driver.refresh()
time.sleep(1)
driver.add_cookie(cookie_li[1])
driver.refresh()
time.sleep(1)
driver.add_cookie(cookie_li[2])
driver.refresh()
time.sleep(1)
print('login successfully')
try:
    if driver.find_element_by_xpath('//span[@class="zbyDdwb"]'):
        driver.find_element_by_xpath('//a[@class="filename"]').click()
        driver.implicitly_wait(10)
        elements = driver.find_elements_by_xpath('//dd[@_installed="1"]')
        for element in elements:
            element.find_element_by_xpath('.//span[@node-type="EOGexf"]').click()
            time.sleep(0.5)
            driver.find_element_by_xpath('//em[@class="icon icon-download"]').click()
            time.sleep(0.5)
            element.find_element_by_xpath('.//span[@node-type="EOGexf"]').click()
            print('download try')
            time.sleep(1)
except:
    driver.find_element_by_xpath('//em[@class="icon icon-download"]').click()
    print('download except')
    time.sleep(1)
driver.implicitly_wait(1000)
print('download sucessfully')
time.sleep(5)
driver.quit()
