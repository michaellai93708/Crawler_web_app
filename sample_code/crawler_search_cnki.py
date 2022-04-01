from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import re
import datetime
import time 
import mysql
import mysql.connector
mysql_connection = mysql.connector.connect(user = 'root', password = 'Laijiachong1', host = 'localhost',database = 'crawler' )
cursor = mysql_connection.cursor()
sql_insert = "INSERT INTO results_1 (Title, Link, Author, Tag, Date) VALUES (%s, %s, %s, %s, %s)"

if __name__ == '__main__':
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=4000,1600")
    driver = webdriver.Chrome(options=chrome_options)
    url = 'https://kns.cnki.net/kns8/AdvSearch?dbprefix=SCDB&&crossDbcodes=CJFQ%2CCDMD%2CCIPD%2CCCND%2CCISD%2CSNAD%2CBDZK%2CCJFN%2CCCJD' 
    driver.get(url)
    driver.implicitly_wait(5)
    driver.maximize_window()
    driver.implicitly_wait(5)
    
    driver.find_element_by_xpath('//span[@value="SU"]').click()
    driver.implicitly_wait(5)
    type_ = '主题'
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
    keyword = '智慧城市'
    input_section = driver.find_element_by_xpath('//div[@class = "input-box"]')
    driver.implicitly_wait(5)
    input_section.find_element_by_xpath(".//input").send_keys(keyword)
    driver.implicitly_wait(5)
    #输入关键字
    driver.find_element_by_xpath('//input[@value="中英文对照"]').click()
    driver.implicitly_wait(5)
    expansion = "topic_expand"
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
    accuracy = 'vague'
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

    search_result_box =  driver.find_element_by_xpath('//div[@class = "search-result"]')
    elements = search_result_box.find_elements_by_tag_name('tr')
    elements.pop(0)
    
    for element in elements:
        title = element.find_element_by_xpath('.//a[@class = "fz14"]').text
        title_final = title.strip()
        
        authors = element.find_element_by_xpath('.//td[@class = "author"]').text
        
        tag = element.find_element_by_xpath('.//td[@class = "source"]').text
        tag_final = tag.strip()

        date = element.find_element_by_xpath('.//td[@class = "date"]').text
        
        if re.search('\d+:', date):
            z = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M').date()
            
        else: 
            z = datetime.datetime.strptime(date,'%Y-%m-%d').date()
        
        

        result = (title_final, None, authors, tag_final, z)
        print(result)
        cursor.execute(sql_insert,result)
        mysql_connection.commit()
    
    driver.close()
    #article_specific_result = article.objects.order_by('Author')
    #THIS SHOULD BE INSIDE IF STATEMENT IF THERE IS ONE 
    
    

   


    

