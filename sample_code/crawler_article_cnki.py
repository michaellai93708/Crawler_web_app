from selenium import webdriver
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


def cnki():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=4000,1600")
    chrome_options.add_argument('disable-javascrip')
    chrome_options.add_argument('disable-images')
    #chrome_options.add_argument("--proxy-server=http://183.6.116.33")
    driver = webdriver.Chrome(options=chrome_options)
    url = 'https://www.cnki.net' 
    driver.get(url)
    driver.find_element_by_xpath('//input[@class = "search-input"]').send_keys('智慧城市')
    driver.find_element_by_xpath('//input[@class = "search-btn"]').click()
    #url = url_prefix + '智慧城市'
    #cursor.execute("DELETE FROM results_1")
    #mysql_connection.commit()
    #print(url)
    
    driver.implicitly_wait(10)
    #print(driver)
    elements = driver.find_elements_by_tag_name("tr")
    elements.pop(0)
    #print(elements[0].text)
    for element in elements:    
        title = element.find_element_by_xpath('.//a[@class = "fz14"]').text
        title_final = title.strip()
        authors = element.find_element_by_xpath('.//td[@class = "author"]').text
        #print(authors)
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
        #print(link)
        print(title_final, authors, date_final)
    driver.close()


if __name__ == '__main__':
    cnki()