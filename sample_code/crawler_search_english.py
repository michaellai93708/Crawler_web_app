from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from translate import Translator
import time
import re
import datetime
import mysql
import mysql.connector

translator_to_chinese = Translator(to_lang="chinese")
translator_to_english = Translator(from_lang="chinese",to_lang="english")
mysql_connection = mysql.connector.connect(user = 'root', password = 'Laijiachong1', host = 'localhost',database = 'crawler' )
cursor = mysql_connection.cursor()
sql_insert = "INSERT INTO results_1 (Title, Link, Author, Tag, Date) VALUES (%s, %s, %s, %s, %s)"

if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument("headless")
    chrome_options.add_argument("--window-size=4000,1600")
    driver = webdriver.Chrome(options=chrome_options)
    url = 'https://www.sciencedirect.com' 
    driver.get(url)
    driver.implicitly_wait(5)
    driver.maximize_window()
    driver.implicitly_wait(5)
    keyword_chn = '智慧城市'
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
                time_format = datetime.datetime.strptime(date_text,'%d %B %Y')
                #print(time_format)
                date = time_format.strftime("%Y-%m-%d")
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
        print(result)
    driver.close()