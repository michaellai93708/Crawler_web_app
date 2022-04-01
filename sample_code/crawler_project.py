from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from pathlib import Path
import pandas as pd
import os
import time
import re
import datetime
import threading 
import json
import urllib.request

def crawler_project_bid():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=8000,7000")
    chrome_options.add_argument('disable-javascrip')
    prefs = {"download.default_directory": "/Users/michael/Downloads"}
    #prefs = {'download.default_directory' : '/Users/michael/Downloads'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome("chromedriver", 0, options=chrome_options)
    driver.get('http://www.ebiaoxun.com/search?keywords=')
    #driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    #params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': '/Users/michael/Downloads'}}
    #driver.execute("send_command", params)
    cookie_path = '/Users/michael/Desktop/Work/project/cookie.txt'
    with open(cookie_path, 'r', encoding='utf-8') as f:
        cookies = f.readlines() 
    for cookie in cookies:
        cookie=cookie.replace(r'\n', '')
        cookie_li = json.loads(cookie)
        driver.implicitly_wait(10)
    for cookie in cookie_li:
        driver.add_cookie(cookie)
        driver.refresh()
    try:
        input_ = driver.find_element_by_xpath('//input[@id="keywords"]').send_keys('交通大脑')
        click_button = driver.find_element_by_xpath('//i[@class="iconfont sou"]').click()
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//em[@class="iconfont chahao"]').click()
        driver.implicitly_wait(5)
        page_section = driver.find_element_by_xpath('//div[@class="pagination-inner fr"]')
        page_down_button = page_section.find_element_by_xpath('.//a[@class="nbnext"]')
        print('first try')
    except:
        driver.refresh()
        page_section = driver.find_element_by_xpath('//div[@class="pagination-inner fr"]')
        page_down_button = page_section.find_element_by_xpath('.//a[@class="nbnext"]')
        print('first except')
    while page_down_button != None:
        #time.sleep(3)
        page_section = driver.find_element_by_xpath('//div[@class="pagination-inner fr"]')
        page_down_button = page_section.find_element_by_xpath('.//a[@class="nbnext"]')
        driver.implicitly_wait(5)
        js_top = "var q=document.documentElement.scrollTop=0"
        driver.execute_script(js_top)
        driver.implicitly_wait(5)
        result_boxes = driver.find_elements_by_xpath('//div[@class="liLuceneList"]')
        driver.implicitly_wait(5)
        #print(len(result_boxes))
        for result_box in result_boxes:
            driver.implicitly_wait(5)
            driver.execute_script('window.scrollBy(0,10)')
            driver.implicitly_wait(5)
            try:
                #time.sleep(3)
                driver.implicitly_wait(5)
                result_box.find_element_by_xpath('.//a[@class="bid_name"]').click()
                driver.implicitly_wait(5)
            except  NoSuchElementException:
                driver.refresh()
                #time.sleep(3)
                driver.implicitly_wait(5)
                result_box.find_element_by_xpath('.//a[@class="bid_name"]').click()
                driver.implicitly_wait(5)
            except:
                continue
            handles_ = driver.window_handles
            driver.switch_to.window(handles_[1])
            driver.implicitly_wait(5)
            try:
                driver.implicitly_wait(5)
                download_section = driver.find_element_by_xpath('//div[@class="proright"]')
                #time.sleep(2)
                download_section.find_element_by_xpath('.//span[@onclick="downloadExcel()"]').click()
                #download_link = download_section.find_element_by_xpath('.//span[@onclick="downloadExcel()"]')
                #print(download_link)
                time.sleep(0.5)
                print('run (second) try')
                driver.implicitly_wait(5)
            except  NoSuchElementException:
                driver.refresh()
                driver.implicitly_wait(5)
                download_section = driver.find_element_by_xpath('//div[@class="proright"]')
                #time.sleep(2)
                download_section.find_element_by_xpath('.//span[@onclick="downloadExcel()"]').click()
                #download_link = download_section.find_element_by_xpath('.//span[@onclick="downloadExcel()"]')
                #print(download_link)
                print('run (second) except')
                driver.implicitly_wait(5)
            except:
                continue
            driver.implicitly_wait(10)
            handles = driver.window_handles
            for n in range(len(handles)):
                #print(n)
                if n == 0:
                    continue
                try:
                    driver.switch_to.window(handles[n])
                    driver.implicitly_wait(5)
                    driver.close()
                    print('third try')
                except:
                    print('third except')
                    continue
            driver.implicitly_wait(5)
            driver.switch_to.window(handles_[0]) 
            driver.implicitly_wait(5)

      
        try:
            driver.execute_script("window.scrollBy(0, 1000)")
            page_section = driver.find_element_by_xpath('//div[@class="pagination-inner fr"]')
            page_section.find_element_by_xpath('.//a[@class="nbnext"]').click()
            driver.implicitly_wait(5)
        except:
            break
        #print('continue')
        #print(page_down_button.get_attribute('class'))
        driver.implicitly_wait(10)
        driver.implicitly_wait(20)
    driver.quit()

def merge_excel_smart_city():
    excel_dir = Path("/Users/michael/Downloads/smart_city")
    excel_files = excel_dir.glob('*.xls')
    df = pd.DataFrame()
    for xls in excel_files:
        data = pd.read_excel(xls)
        df = df.append(data)
        os.remove(xls)
    df.to_excel(excel_dir/ "smart_city/output_smart_city.xlsx", index = False)
#MERGE EXCEL FILE SMART CITY
def merge_excel_smart_transit():
    excel_dir = Path("/Users/michael/Downloads/smart_transit")
    excel_files = excel_dir.glob('*.xls')
    df = pd.DataFrame()
    for xls in excel_files:
        data = pd.read_excel(xls)
        df = df.append(data)
        os.remove(xls)
    df.to_excel(excel_dir / "smart_transit/output_smart_transit.xlsx", index = False)
#MERGE EXCEL FILE SMART TRANSIT
def crawler_project_bidder():
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
    cookie_path = '/Users/michael/Desktop/Work/project/cookie.txt'
    #time.sleep(10)#等待扫码时间
    with open(cookie_path, 'r', encoding='utf-8') as f:
        cookies = f.readlines() 
    for cookie in cookies:
        cookie=cookie.replace(r'\n', '')
        cookie_li = json.loads(cookie)
        time.sleep(3)
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
    #time.sleep(10)
    driver.find_element_by_xpath('//input[@value="中标企业搜索"]').click()
    driver.find_element_by_xpath('//input[@class="searchname"]').send_keys('阿里云计算有限公司')
    driver.implicitly_wait(5)
    enter = driver.find_element_by_xpath('//button[@id="serBtn"]')
    driver.implicitly_wait(50)
    enter.send_keys(Keys.ENTER)
    driver.implicitly_wait(50)
    time.sleep(5)
    driver.find_element_by_xpath('//em[@class="iconfont chahao"]').click()
    driver.implicitly_wait(5)
    page_section = driver.find_element_by_xpath('//div[@class="pagination-inner fr"]')
    page_down_button = page_section.find_element_by_xpath('.//a[@class="nbnext"]')
    while page_down_button != None:
        driver.implicitly_wait(5)
        js_top = "var q=document.documentElement.scrollTop=0"
        driver.execute_script(js_top)
        driver.implicitly_wait(5)
        result_boxes = driver.find_elements_by_xpath('//tr[@class="qiyetr"]')
        driver.implicitly_wait(5)
        
        #print(len(result_boxes))
        for result_box in result_boxes:
            driver.implicitly_wait(5)
            driver.execute_script('window.scrollBy(0,10)')
            driver.implicitly_wait(5)
            time.sleep(2)
            result_box.find_element_by_xpath('.//a[@onclick="noIn(this)"]').click()
            driver.implicitly_wait(5)
            handles_ = driver.window_handles
            driver.switch_to.window(handles_[1])
            download_section = driver.find_element_by_xpath('//div[@class="proright"]')
            driver.implicitly_wait(5)
            download_section.find_element_by_xpath('.//span[@onclick="downloadExcel()"]').click()
            driver.implicitly_wait(5)
            time.sleep(0.5)
            handles = driver.window_handles
            for n in range(len(handles)):
                if n == 0:
                    continue
                driver.switch_to.window(handles[n])
                driver.implicitly_wait(5)
                driver.close()
            driver.implicitly_wait(5)
            driver.switch_to.window(handles_[0]) 
            driver.implicitly_wait(5)
        time.sleep(1.5)
        if page_down_button.get_attribute('style') == 'display: none;':
            #print('break')
            break
        driver.execute_script("window.scrollBy(0, 1000)")
        page_section = driver.find_element_by_xpath('//div[@class="pagination-inner fr"]')
        page_section.find_element_by_xpath('.//a[@class="nbnext"]').click()
        driver.implicitly_wait(5)
        #print('continue')
        #print(page_down_button.get_attribute('class'))
        time.sleep(1)
    driver.quit() 
    time.sleep(0.1)
    merge_excel_ali()
#PROJECT BIDDER NAME
def merge_excel_ali():
    excel_dir = Path("/Users/michael/Downloads/ali")
    excel_files = excel_dir.glob('*.xls')
    df = pd.DataFrame()
    for xls in excel_files:
        data = pd.read_excel(xls)
        df = df.append(data)
        os.remove(xls)
    df.to_excel(excel_dir/ "ali/output_ali.xlsx", index = False)
#MERGE EXCEL FILE ALI 

if __name__ == '__main__':
   #crawler_project_bid()
   crawler_project_bidder()

