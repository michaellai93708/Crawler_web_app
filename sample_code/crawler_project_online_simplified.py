from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from apscheduler.schedulers.blocking import BlockingScheduler
from pathlib import Path
import pandas as pd
import os
import time
import re
import datetime
import threading
import json
import mysql
import mysql.connector
import xlrd
import urllib.request


def crawler_project_bidder():
    keyword_bidder_list = ['阿里云计算有限公司', '华为技术有限公司']
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    #chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--disable-dev-shm-usage')
    #chrome_options.add_argument('blink-settings=imagesEnabled=false')
    #chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--window-size=8000,7000")
    #chrome_options.add_argument('disable-javascrip')
    prefs = {'download.default_directory' : '/Users/michael/Downloads'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome("chromedriver", 0, options=chrome_options)
    driver.get('http://www.ebiaoxun.com/search?keywords=')
    cookie_path = '/Users/michael/Desktop/Work/project/cookie.txt'
    with open(cookie_path, 'r', encoding='utf-8') as f:
        cookies = f.readlines() 
    for cookie in cookies:
        cookie=cookie.replace(r'\n', '')
        cookie_li = json.loads(cookie)
        driver.implicitly_wait(5)
    driver.add_cookie(cookie_li[0])
    driver.refresh()
    time.sleep(1)
    driver.add_cookie(cookie_li[1])
    driver.refresh()
    time.sleep(1)
    driver.add_cookie(cookie_li[2])
    driver.refresh()
    time.sleep(1)
    driver.find_element_by_xpath('//i[@class="iconfont sou"]').click()
    #driver.refresh()
    for keyword in keyword_bidder_list:
        #time.sleep(30)
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//input[@value="中标企业搜索"]').click()
        driver.find_element_by_xpath('//input[@class="searchname"]').send_keys(keyword)
        driver.implicitly_wait(5)
        enter = driver.find_element_by_xpath('//button[@id="serBtn"]')
        driver.implicitly_wait(50)
        enter.send_keys(Keys.ENTER)
        time.sleep(3)
        capcha = driver.find_element_by_xpath('//div[@class="modal-content"]')
        img = driver.find_element_by_xpath('//img[@id="img_verify"]')
        img_url = img.get_attribute('src')  
        #print('save png')
        #if img_url: 
           
        #print('png saved')
            #js = "window.open('https://sc.ftqq.com/SCU153285T701c6289e7322f80c6b064335a627bf3600a38d3bb36c.send?text=http://ebspider.top:8000/cap')"
            #driver.execute_script(js)
            #handles_ = driver.window_handles
            #driver.switch_to.window(handles_[1])
            #time.sleep(10)
            #handles = driver.window_handles
            #for n in range(len(handles)):
            #    if n == 0:
            #        continue
            #    driver.switch_to.window(handles[n])
            #    driver.implicitly_wait(5)
            #    driver.close()
            #driver.implicitly_wait(5)
            #driver.switch_to.window(handles_[0]) 
            #driver.implicitly_wait(5)
        #print('check cap websige')
        #time.sleep(30)

           
            #cursor.execute("SELECT 验证码 FROM app_project_captcha")
            #value = cursor.fetchall()
            #values = cursor.fetchall()
            #captchas = []
            #for value in values:
            #    captchas.append(value[0])
            #for captcha in captchas :
            #    print(captcha)
            
        time.sleep(1)
    
        driver.implicitly_wait(50)
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//em[@class="iconfont chahao"]').click()
        driver.implicitly_wait(10)
        page_section = driver.find_element_by_xpath('//div[@class="pagination-inner fr"]')
        page_down_button = page_section.find_element_by_xpath('.//a[@class="nbnext"]')
        print('successfully input search word')
        time.sleep(3)
        while page_down_button != None:
            page_section = driver.find_element_by_xpath('//div[@class="pagination-inner fr"]')
            page_down_button = page_section.find_element_by_xpath('.//a[@class="nbnext"]')
            driver.implicitly_wait(5)
            js_top = "var q=document.documentElement.scrollTop=0"
            driver.execute_script(js_top)
            driver.implicitly_wait(5)
            try:
                time.sleep(3)
                result_boxes = driver.find_elements_by_xpath('//tr[@class="qiyetr"]')
                driver.implicitly_wait(5)
            except:
                print('no result box found')
                break
            #print(len(result_boxes))
            for result_box in result_boxes:
                driver.implicitly_wait(100)
                driver.execute_script('window.scrollBy(0,10)')
                driver.implicitly_wait(5)
                try:
                    time.sleep(1)
                    driver.implicitly_wait(5)
                    result___ = result_box.find_element_by_xpath('.//a[@onclick="noIn(this)"]')
                    print(result___)
                    driver.implicitly_wait(5)
                    print('sucessfully open a the bidder tab')
                except:
                    print('fail to open bidder tab')
                    continue
                
            try:
                driver.execute_script("window.scrollBy(0, 1000)")
                page_section = driver.find_element_by_xpath('//div[@class="pagination-inner fr"]')
                page_section.find_element_by_xpath('.//a[@class="nbnext"]').click()
                driver.implicitly_wait(5)
            except:
                break
        
        #print('continue')
        #print(page_down_button.get_attribute('class'))
        js_top = "var q=document.documentElement.scrollTop=0"
        driver.execute_script(js_top)
    driver.quit() 
# 中标方



if __name__ == '__main__':
    #cursor.execute("DELETE FROM app_project_chn_bid")
    #mysql_connection.commit()
    #cursor.execute("DELETE FROM app_project_chn_simplified_bid")
    #mysql_connection.commit()

    crawler_project_bidder()
    #try:
    #    schedule_job()
    #except:
    #    print('fail')
    
        

#def excel_remove_duplicate_bid():
#    frame = pd.read_excel('/root/python/Downloads/bid/out.xlsx')
#    data = pd.DataFrame(frame)
#    data.drop_duplicates(['信息标题', '招标编号'], keep='first', inplace=True)
#    # drop_duplicates用法：subset=‘需要去重复的列名’,keep=‘遇到重复的时保留第一个还是保留最后一个’,inplace=‘去除重复项，还是保留重复项的副本’
#    data.to_excel('/root/python/Downloads/bid/output.xlsx')
#    #print('合并完成')
## REMOVE EXCEL DUPLICATE BID
#def excel_remove_duplicate_bidder():
#    frame = pd.read_excel('/root/python/Downloads/bidder/out.xlsx')
#    data = pd.DataFrame(frame)
#    data.drop_duplicates(['信息标题', '招标编号'], keep='first', inplace=True)
#    # drop_duplicates用法：subset=‘需要去重复的列名’,keep=‘遇到重复的时保留第一个还是保留最后一个’,inplace=‘去除重复项，还是保留重复项的副本’
#    data.to_excel('/root/python/Downloads/bidder/output.xlsx')
#    #print('合并完成')
## REMOVE EXCEL DUPLICATE BIDDER