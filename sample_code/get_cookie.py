from selenium import webdriver
import json
import time 

cookie_path = 'cookie.txt'
browser = webdriver.Chrome()
browser.get('https://pan.baidu.com/s/1kqBm_nzk23K9xiCpP7pEwg')
time.sleep(60)
cookie = browser.get_cookies()

with open(cookie_path, 'w', encoding='utf-8') as f:
    f.writelines(json.dumps(cookie) + r'\n')
# 链接: https://pan.baidu.com/s/1VrvjI0OMBO6yD4Sj2V84sg 提取码: 8utf 复制这段内容后打开百度网盘手机App，操作更方便哦