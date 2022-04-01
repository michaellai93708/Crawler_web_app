from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from app.models import result_b, Trie, article
from django.db.models import Q
from django.http import FileResponse
from django.core.paginator import Paginator, Page, EmptyPage, PageNotAnInteger
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.chrome.options import Options
from translate import Translator
from pathlib import Path
import pandas as pd
import os
import mysql
import mysql.connector
import time
import re
import datetime
import threading 

translator_to_chinese = Translator(to_lang="chinese")
translator_to_english = Translator(from_lang="chinese",to_lang="english")
#翻译
mysql_connection = mysql.connector.connect(user = 'root', password = 'Laijiachong1', host = 'localhost',database = 'crawler' )
cursor = mysql_connection.cursor()
sql_insert = "INSERT INTO app_article (Title, Link, Author, Tag, Date) VALUES (%s, %s, %s, %s, %s)"
#论文结果插入mysql
# Create your views here.
def crawler_wanfang_specific(type_, accuracy, keyword, expansion):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=4000,1600")
    driver = webdriver.Chrome(options=chrome_options)
    url = 'http://www.wanfangdata.com.cn/searchResult/getAdvancedSearch.do?searchType=all' 
    driver.get(url)
    driver.implicitly_wait(3.5)
    #driver.find_element_by_xpath('//a[@id="zh_click_s"]').click()
    
    #wanfang()
    #print(time_convert('2016(学位年度)'))
    
    driver.find_element_by_xpath('//div[@class="ctrl-text all"]').click()
    driver.implicitly_wait(3.5)
    #全选
    search_field_section = driver.find_element_by_xpath('//div[@class="search-option field ivu-select ivu-select-single ivu-select-default"]')
    driver.implicitly_wait(3.5)
    search_field_section.find_element_by_xpath('.//span[@class="ivu-select-selected-value"]').click()
    time.sleep(1)
    fields = search_field_section.find_elements_by_xpath(".//li[@class='ivu-select-item']")
    driver.implicitly_wait(3.5)
    
    #input_ = '作者'
    if type_ == '主题':
        search_field_section.find_element_by_xpath('.//li[@class="ivu-select-item ivu-select-item-selected"]').click()
        driver.implicitly_wait(3.5)
        
    elif type_  == '全部':
        driver.implicitly_wait(3.5)
        fields[0].click()
    elif type_  == '题名':
        driver.implicitly_wait(3.5)
        fields[2].click()
    elif type_  == '作者':
        driver.implicitly_wait(3.5)
        fields[3].click()
    elif type_  == '作者单位':
        driver.implicitly_wait(3.5)
        fields[4].click()
    elif type_  == '关键词':
        driver.implicitly_wait(3.5)
        fields[5].click()
    elif type_  == '摘要':
        driver.implicitly_wait(3.5)
        fields[6].click()
    elif type_  == '中图分类号':
        driver.implicitly_wait(3.5)
        fields[7].click()
    elif type_  == 'DOI':
        driver.implicitly_wait(3.5)
        fields[8].click()
    elif type_  == '第一作者':
        driver.implicitly_wait(3.5)
        fields[9].click()
    driver.implicitly_wait(3.5)
    #检索信息
    accuracy_section = driver.find_element_by_xpath('//div[@class="search-option ivu-select ivu-select-single ivu-select-default"]')
    driver.implicitly_wait(3.5)
    accuracy_section.find_element_by_xpath('.//span[@class="ivu-select-selected-value"]').click()
    driver.implicitly_wait(3.5)
    #accuracy = '模糊'
    if accuracy == 'accurate':
        driver.implicitly_wait(3.5)
        selected = accuracy_section.find_element_by_xpath(".//li[@class='ivu-select-item']").click()
    else:
        driver.implicitly_wait(3.5)
        selected = accuracy_section.find_element_by_xpath(".//li[@class='ivu-select-item ivu-select-item-selected']").click()
    #精确度
    input_section = driver.find_element_by_xpath('//div[@class="value-input ivu-input-wrapper ivu-input-wrapper-default ivu-input-type-text"]')
    driver.implicitly_wait(3.5)
    #keyword = '智慧城市'
    driver.implicitly_wait(3.5)
    input_section.find_element_by_xpath('.//input[@class="ivu-input ivu-input-default"]').send_keys(keyword)
    driver.implicitly_wait(3.5)
    #搜索词条
    expansion_section = driver.find_element_by_xpath('//div[@class="time-select"]')
    driver.implicitly_wait(3.5)
    expansion_list = expansion_section.find_elements_by_xpath('.//span[@class="resource-item"]')
    driver.implicitly_wait(3.5)
    #expansions = ["chinese_english_expand", "topic_expand" ]
    if expansion == "chinese_english_expand":
            #print(expansion_list[0].text)
            expansion_list[0].click()
            driver.implicitly_wait(3.5)
    elif expansion == "topic_expand":
            #print(expansion_list[1].text)
            expansion_list[1].click()
            driver.implicitly_wait(3.5)
        
    #中英文次或主题词扩展
    submit_section = driver.find_element_by_xpath('//div[@class="submit"]')
    driver.implicitly_wait(3.5)
    submit_section.find_element_by_xpath('.//span[@class="submit-btn"]').click()
    driver.implicitly_wait(3.5)
    #点击搜索按钮
    elements = driver.find_elements_by_class_name("normal-list")
    #print(len(elements))
    for element in elements:
        title = element.find_element_by_xpath('.//a[@class="title"]').text
        #print(title)

        link = element.find_element_by_xpath('.//a[@class="title"]').get_attribute('href')
        #print(link)

        authors = element.find_elements_by_xpath('.//span[@class="authors"]')
        author = []
        for i in range(len(authors)):
            author_pending =  authors[i].text
            #print(author_pending)
            if re.match('\d+', author_pending):
                continue
            author.append(author_pending)
        author_final = (', '.join(str(x) for x in author))
        #print(author_final)

        tags = element.find_elements_by_xpath('.//span[@class="keywords-list"]')
        tag = []
        for i in range(len(tags)):
            tag.append(tags[i].text)
        tag_final = (', '.join(str(x) for x in tag))
        #print(tag_final)

        date = '于' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '获取'
        #print(date)
        result = (title, link, author_final, tag_final, date)
        cursor.execute(sql_insert,result)
        mysql_connection.commit()
        #print(result)
    driver.quit()
    time.sleep(0.5)
#SPECIFIC ARTICLE SEARCH WANFANG
def crawrler_cnki_specific(type_, accuracy, keyword, expansion):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=4000,1600")
    driver = webdriver.Chrome(options=chrome_options)
    url = 'https://kns.cnki.net/kns8/AdvSearch?dbprefix=SCDB&&crossDbcodes=CJFQ%2CCDMD%2CCIPD%2CCCND%2CCISD%2CSNAD%2CBDZK%2CCJFN%2CCCJD' 
    driver.get(url)
    driver.implicitly_wait(5)
    #driver.maximize_window()
    #driver.implicitly_wait(5)
    
    driver.find_element_by_xpath('//span[@value="SU"]').click()
    driver.implicitly_wait(5)
    
    if  type_ == '关键词':
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//a[@value="KY"]').click()
    elif  type_ == '题名':
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//a[@value="TI"]').click()
    elif  type_ == '作者':
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//a[@value="AU"]').click()
    elif  type_ == '第一作者':
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//a[@value="FI"]').click()
    elif  type_ == '作者单位':
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//a[@value="AF"]').click()
    elif  type_ == '摘要':
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//a[@value="AB"]').click()
    elif  type_ == 'DOI':
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//a[@value="DOI$=|?"]').click()
    elif  type_ == '中图分类号':
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//a[@value="CLC$=|??"]').click()
    driver.implicitly_wait(5)
    #检索信息
    
    
    driver.find_element_by_xpath('//input[@data-tipid="gradetxt-1"]').send_keys(keyword)
    driver.implicitly_wait(5)
    #输入关键字
    driver.find_element_by_xpath('//input[@value="中英文对照"]').click()
    driver.implicitly_wait(5)
    
    check_box_extend_section = driver.find_element_by_xpath('//span[@class="extend-label"]')
    driver.implicitly_wait(5)
    if expansion == "chinese_english_expand":
        check_box_extend_section.find_element_by_xpath('.//input[@value="中英文对照"]').click()
        driver.implicitly_wait(5)
    elif expansion == "topic_expand":
        check_box_extend_section.find_element_by_xpath('.//input[@value="SYS_XL_SYNONYM_DICT"]').click()
        driver.implicitly_wait(5)
    #扩展
    accuracy_section = driver.find_element_by_xpath('//div[@class="sort special"]')
    driver.implicitly_wait(5)
    
    driver.implicitly_wait(5)
    if type_ != '主题':
        if accuracy == 'vague':
            driver.implicitly_wait(5)
            accuracy_section.find_element_by_xpath('.//div[@class="sort-default"]').click()
            driver.implicitly_wait(5)
            accuracy_section.find_element_by_xpath('.//a[@value="%"]').click()
    #精确度
    driver.implicitly_wait(5)
    driver.find_element_by_xpath('//input[@value="检索"]').click()
    driver.implicitly_wait(5)
    #点击搜索按钮
    try:
        search_result_box =  driver.find_element_by_xpath('//div[@class = "search-result"]')
        elements = search_result_box.find_elements_by_tag_name('tr')
        elements.pop(0)
    
        for element in elements:
            title = element.find_element_by_xpath('.//a[@class = "fz14"]').text
            title_final = title.strip()
        
            authors = element.find_element_by_xpath('.//td[@class = "author"]').text
        
            tag = '本网页没有标签'

            date = element.find_element_by_xpath('.//td[@class = "date"]').text
        
            if re.search('\d+:', date):
                z = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M').date()
            
            else: 
                z = datetime.datetime.strptime(date,'%Y-%m-%d').date()
            #link_click = element.find_element_by_xpath('.//td[@class = "name"]').click()
            #handles_ = driver.window_handles
            #driver.switch_to.window(handles_[1])
            #link = driver.current_url
            #driver.close()
            #driver.switch_to.window(handles_[0])
            link = None
            result = (title_final, link, authors, tag, z)
            #print(result)
            cursor.execute(sql_insert,result)
            mysql_connection.commit()
        driver.quit()
    except:
        driver.quit()
        article_specific_result = ('查无结果')
#SPECIFIC ARTICLE SEARCH CNKI
def crawler_wanfang(keyword):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=4000,1600")
    chrome_options.add_argument('disable-javascrip')
    chrome_options.add_argument('disable-images')
    driver = webdriver.Chrome(options=chrome_options)
    url_prefix = 'http://s.wanfangdata.com.cn/paper?q=' 
    url = url_prefix + keyword
    driver.get(url)
    time.sleep(1)
    elements = driver.find_elements_by_class_name("normal-list")
    #print(elements)
    for element in elements:
        title = element.find_element_by_xpath('.//a[@class="title"]').text
        #print(title)

        link = element.find_element_by_xpath('.//a[@class="title"]').get_attribute('href')
        #print(link)

        authors = element.find_elements_by_xpath('.//span[@class="authors"]')
        author = []
        for i in range(len(authors)):
            author_pending =  authors[i].text
            #print(author_pending)
            if re.match('\d+', author_pending):
                continue
            author.append(author_pending)
        author_final = (', '.join(str(x) for x in author))
        #print(author_final)

        tags = element.find_elements_by_xpath('.//span[@class="keywords-list"]')
        tag = []
        for i in range(len(tags)):
            tag.append(tags[i].text)
        tag_final = (', '.join(str(x) for x in tag))
        #print(tag_final)

        date = '于' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '获取'
        #print(date)
        result = (title, link, author_final, tag_final, date)
        cursor.execute(sql_insert,result)
        mysql_connection.commit()
    driver.find_element_by_xpath('//span[@class="next"]').click()
    driver.implicitly_wait(5)
    time.sleep(2)
    js_top = "var q=document.documentElement.scrollTop=0"
    driver.execute_script(js_top)
    
    elements = driver.find_elements_by_class_name("normal-list")
    #print(elements)
    for element in elements:
        title = element.find_element_by_xpath('.//a[@class="title"]').text
        #print(title)

        link = element.find_element_by_xpath('.//a[@class="title"]').get_attribute('href')
        #print(link)

        authors = element.find_elements_by_xpath('.//span[@class="authors"]')
        author = []
        for i in range(len(authors)):
            author_pending =  authors[i].text
            #print(author_pending)
            if re.match('\d+', author_pending):
                continue
            author.append(author_pending)
        author_final = (', '.join(str(x) for x in author))
        #print(author_final)

        tags = element.find_elements_by_xpath('.//span[@class="keywords-list"]')
        tag = []
        for i in range(len(tags)):
            tag.append(tags[i].text)
        tag_final = (', '.join(str(x) for x in tag))
        #print(tag_final)

        date = '于' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '获取'
        #print(date)
        result = (title, link, author_final, tag_final, date)
        cursor.execute(sql_insert,result)
        mysql_connection.commit()
    driver.quit()
#REGULAR ARTICLE SEARCH WANFANG
def crawler_cnki(keyword):
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=4000,1600")
    chrome_options.add_argument('disable-javascrip')
    chrome_options.add_argument('disable-images')
    driver = webdriver.Chrome(options=chrome_options)
    url_prefix = 'https://kns8.cnki.net/kns/DefaultResult/Index?dbcode=SCDB&kw=' 
    url = url_prefix + keyword
    #cursor.execute("DELETE FROM results_1")
    #mysql_connection.commit()
    #print(url)
    driver.get(url)
    time.sleep(1)
    #print(driver)
    elements = driver.find_elements_by_tag_name("tr")
    elements.pop(0)
    #print(elements[0].text)
    for element in elements:    
        title = element.find_element_by_xpath('.//a[@class = "fz14"]').text
        title_final = title.strip()
        authors = element.find_element_by_xpath('.//td[@class = "author"]').text
        #print(authors)
        tag = '本网页没有标签'
        date = element.find_element_by_xpath('.//td[@class = "date"]').text
        if re.search('\d+:', date):
            z = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M').date()
        else: 
            z = datetime.datetime.strptime(date,'%Y-%m-%d').date()
        date_final = z
        #link_click = element.find_element_by_xpath('.//td[@class = "name"]').click()
        #handles_ = driver.window_handles
        #driver.switch_to.window(handles_[1])
        #link = driver.current_url
        #driver.close()
        #driver.switch_to.window(handles_[0])
        link = None
        result = (title_final, link, authors, tag, date_final)
        cursor.execute(sql_insert,result)
        mysql_connection.commit()
    driver.quit()
#REGULAR ARTICLE SEARCH CNKI
def crawler_english(keyword_):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=4000,1600")
    chrome_options.add_argument('disable-javascrip')
    chrome_options.add_argument('disable-images')
    driver = webdriver.Chrome(options=chrome_options)
    url = 'https://www.sciencedirect.com' 
    driver.get(url)
    driver.implicitly_wait(5)
    driver.maximize_window()
    driver.implicitly_wait(5)
    keyword_chn = keyword_
    keyword = translator_to_english.translate(keyword_chn)
    driver.implicitly_wait(5)
    driver.find_element_by_xpath('//input[@id="qs-searchbox-input"]').send_keys(keyword)
    driver.implicitly_wait(5)
    driver.find_element_by_xpath('//button[@class="button SearchSubmitButton button-primary"]').click()
    driver.implicitly_wait(5)
    result_section = driver.find_element_by_xpath('//ol[@class="search-result-wrapper"]')
    driver.implicitly_wait(5)
    result_boxes = result_section.find_elements_by_xpath('//li[@class="ResultItem col-xs-24 push-m"]')
    driver.implicitly_wait(5)
    for result_box in result_boxes:
        title = result_box.find_element_by_tag_name('h2').text
        #print(title)

        link = result_box.find_element_by_xpath('.//a[@class="result-list-title-link u-font-serif text-s"]').get_attribute('href')
        #print(link)

        authors = result_box.find_elements_by_xpath('.//span[@class="author"]')
        author = []
        for author_ in authors:
            if author_ == None:
                continue
            author.append(author_.text)
        #print(author)
        
        author = [i for i in author if i != '']
        author_final = (', '.join(str(x) for x in author))
        #print(author_final)
        
        tag = '本网页没有标签'

        date_ = result_box.find_elements_by_xpath('.//span[@class="preceding-comma"]')
        for i in date_:
            if re.match('\d+.+\d+', i.text):
                date_text = i.text
                time_format=datetime.datetime.strptime(date_text,'%d %B %Y')
                #print(time_format)
                date=time_format.strftime("%Y-%m-%d")
                #print(date)
                #date.append(i.text)
            elif re.match('Available online', i.text):
                date_text = i.text
                date_0 = re.search('(\d+.+\d+)', date_text)
                date_text_ = date_0.group(0)
                time_format = datetime.datetime.strptime(date_text_,'%d %B %Y')
                date = time_format.strftime("%Y-%m-%d")
                #time_format=datetime.datetime.strptime(date_text,'%d %B %Y')
                #date = time_format.strftime("%Y-%m-%d")
            else:
                date = i.text
        #print(date)
        result = (title, link, author_final, tag, date)
        cursor.execute(sql_insert, result)
        mysql_connection.commit()
    driver.quit()
#REGULAR ARTICLE SEARCH ENGLISH
def type_analysis(type_):
    if type_ == 'perio':
        category = 'periodical'
        return category
    elif type_ == 'degree':
        category = 'thesis'
        return category
    elif type_ == 'conference':
        category = 'conference'
        return category
    elif type_ == 'patent':
        category = 'patent'
        return category
    elif type_ == 'techResult':
        category = 'cstad'
        return category
    elif type_ == 'standards':
        category = 'standard'
        return category
    elif type_ == 'legislations':
        category = 'claw'
        return category
    elif type_ == 'tech':
        category = 'nstr'
        return category
    else:
        return None
#ANALYZE LINK TYPE FOR WANFANG
def crawler_project():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=8000,7000")
    driver = webdriver.Chrome(options=chrome_options)
    url = 'http://www.ebiaoxun.com/search?keywords=' 
    driver.get(url)
    time.sleep(7.5)#等待扫码时间
    input_ = driver.find_element_by_xpath('//input[@id="keywords"]').send_keys('智慧城市')
    click_button = driver.find_element_by_xpath('//i[@class="iconfont sou"]').click()
    driver.implicitly_wait(5)
    driver.find_element_by_xpath('//em[@class="iconfont chahao"]').click()
    driver.implicitly_wait(5)
    page_section = driver.find_element_by_xpath('//div[@class="pagination-inner fr"]')
    page_down_button = page_section.find_element_by_xpath('.//a[@class="nbnext"]')
    while page_down_button != None:
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
            result_box.find_element_by_xpath('.//a[@class="bid_name"]').click()
            driver.implicitly_wait(5)
            handles_ = driver.window_handles
            driver.switch_to.window(handles_[1])
            download_section = driver.find_element_by_xpath('//div[@class="proright"]')
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
        if page_down_button.get_attribute('style') == 'display: none;':
            #print('break')
            break
        page_down_button.click()
        driver.implicitly_wait(5)
        #print('continue')
        #print(page_down_button.get_attribute('class'))
        time.sleep(1)
    time.sleep(0.2)
    merge_excel_smart_city()
    #MERGE EXCEL FILES FOR SMART CITY
    time.sleep(0.2)
    #FINISHING SEARCHING FOR SMART CITY 
    driver.find_element_by_xpath('//li[@style="margin-right: 45px;"]').click()
    driver.implicitly_wait(5)
    #REDIRECT BACK TO HOMEPAGE
    input_ = driver.find_element_by_xpath('//input[@id="keywords"]').send_keys('智慧交通')
    click_button = driver.find_element_by_xpath('//i[@class="iconfont sou"]').click()
    driver.implicitly_wait(5)
    driver.find_element_by_xpath('//em[@class="iconfont chahao"]').click()
    driver.implicitly_wait(5)
    page_section = driver.find_element_by_xpath('//div[@class="pagination-inner fr"]')
    page_down_button = page_section.find_element_by_xpath('.//a[@class="nbnext"]')
    while page_down_button != None:
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
            result_box.find_element_by_xpath('.//a[@class="bid_name"]').click()
            driver.implicitly_wait(5)
            handles_ = driver.window_handles
            driver.switch_to.window(handles_[1])
            download_section = driver.find_element_by_xpath('//div[@class="proright"]')
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
           
        if page_down_button.get_attribute('style') == 'display: none;':
            #print('break')
            break
        page_down_button.click()
        driver.implicitly_wait(5)
        #print('continue')
        #print(page_down_button.get_attribute('class'))
        time.sleep(1)
    driver.quit() 
    #FINISHING SEARCHING FOR SMART TRANSIT
    time.sleep(0.2)
    merge_excel_smart_transit() 
    #MERGE EXCEL FILES FOR SMART TRANSIT
    time.sleep(0.2)
#PROJECT SEARCH
def merge_excel_smart_city():
    excel_dir = Path("/Users/michael/Downloads")
    excel_files = excel_dir.glob('*.xls')
    df = pd.DataFrame()
    for xls in excel_files:
        data = pd.read_excel(xls)
        df = df.append(data)
        os.remove(xls)
    df.to_excel(excel_dir/ "smart_city/output_smart_city.xlsx", index = False)
#MERGE EXCEL FILE SMART CITY
def merge_excel_smart_transit():
    excel_dir = Path("/Users/michael/Downloads")
    excel_files = excel_dir.glob('*.xls')
    df = pd.DataFrame()
    for xls in excel_files:
        data = pd.read_excel(xls)
        df = df.append(data)
        os.remove(xls)
    df.to_excel(excel_dir / "smart_transit/output_smart_transit.xlsx", index = False)
#MERGE EXCEL FILE SMART TRANSIT
def download_smart_city(request):
    file=open('/Users/michael/Downloads/smart_city/smart_city/output_smart_city.xlsx','rb')
    response =FileResponse(file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="output_smart_city.xlsx"'
    return response
#DOWNLOAD PROJECT EXCEL SMART CITY
def download_smart_transit(request):
    file=open('/Users/michael/Downloads/smart_transit/smart_transit/output_smart_transit.xlsx','rb')
    response =FileResponse(file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="output_smart_transit.xlsx"'
    return response
#DOWNLOAD PROJECT EXCEL SMART TRANSIT
def home(request):
    return render(request, 'app/home.html')
#FUNCTION FOR HOMEPAGE
def index(request):
    results_ = result_b.objects.order_by('-Time')
    paginator = Paginator(results_, 15)
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    return render(request, 'app/index.html', {'results': results})
#FUNCTION FOR NEWS RESULT
def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = 'NO RESULT FOUND'
        return render(request, 'app/errors.html', {'error_msg': error_msg})
    post_list = result_b.objects.filter(Q(Author__icontains=q) | Q(Tag__icontains=q)).order_by('-Time')[:30]
    return render(request, 'app/results.html', {'error_msg': error_msg,
                                               'post_list': post_list})
#FUNCTION FOR NEWS RESULT SEARCH
def trie_search(request):
    q = request.GET.get('name')
    cursor.execute('SELECT*FROM crawler.app_trie WHERE name =%s', (q,))
    id_ = [item[0] for item in cursor.fetchall()]
    
    SELECT_DISTINCT = 'SELECT DISTINCT app_result_b.Title,app_result_b.Time,app_result_b.Author,app_result_b.Tag,app_result_b.Link FROM app_result_b, app_trie where instr(app_result_b.Tag,app_trie.name)>0 AND parent_id = %s limit 30'
    cursor.execute(SELECT_DISTINCT, (id_[0],))
    result_list = cursor.fetchall()
    return render(request, 'app/trie_search.html', {'result_list': result_list})
#FUNCTION FOR TRIE SEARCH FOR NEWS
def article_home(request):
    return render(request, 'app/article_home.html')
#FUNCTION FOR ARTICLE HOME(SEARCH PAGE REGULAR)
def article_search(request):
    q = request.GET.get('q')
    cursor.execute("DELETE FROM app_article")
    mysql_connection.commit()
    threads = []
    t1 = threading.Thread(target=crawler_wanfang, args = (q,))
    threads.append(t1)
    t2 = threading.Thread(target=crawler_cnki, args = (q,))
    threads.append(t2)
    t3 = threading.Thread(target=crawler_english, args = (q,))
    threads.append(t3)
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    #time.sleep(5)
    article_result_list = article.objects.order_by('Author')
    return render(request, 'app/article_result.html', {'article_result_list': article_result_list})
#FUNCTION FOR ARTICLE SEARCH(REGULAR)
def article_search_specific_home(request):
    return render(request, 'app/article_search_specific_home.html')    
#FUNCTION FOR ARTICLE HOME SPECIFIC
def article_search_specific(request):
    type_ = request.POST.get('类型')
    accuracy = request.POST.get('精确度')
    keyword =  request.POST.get('搜索词')
    expansion = request.POST.get('扩展')
    cursor.execute("DELETE FROM app_article")
    mysql_connection.commit()
    threads = []
    t1 = threading.Thread(target=crawler_wanfang_specific, args = (type_, accuracy, keyword, expansion))
    threads.append(t1)
    t2 = threading.Thread(target=crawrler_cnki_specific, args = (type_, accuracy, keyword, expansion))
    threads.append(t2)
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    article_specific_result = article.objects.order_by('Author')
    return render(request, 'app/article_specific_result.html', {'article_specific_result': article_specific_result})
#FUNCTION FOR ARTICLE SEARCH SPECIFIC 
def project_search_home(request):
    return render(request, 'app/project_home.html')    
#FUNCTION FOR PROJECT HOME 
def project_search(request):
   #crawler_project()
   return render(request, 'app/project.html')
#FUNCTION FOR PROJECT SEARCH