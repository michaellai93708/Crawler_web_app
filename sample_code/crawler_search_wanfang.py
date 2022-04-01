from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException  
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
    cursor.execute("DELETE FROM results_1")
    mysql_connection.commit()
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=4000,1600")
    chrome_options.add_argument('disable-javascrip')
    driver = webdriver.Chrome(options=chrome_options)
    url_prefix = 'http://s.wanfangdata.com.cn/paper?q=' 
    url = url_prefix + '智慧城市'
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
