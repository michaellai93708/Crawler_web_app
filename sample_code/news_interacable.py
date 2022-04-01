from urllib.request import urlopen, urljoin 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import mysql
import mysql.connector
import datetime
import re 

def func(z):
    year = z.split('年')[0]
    #print(year)
    month = z.split('年')[1].split("月")[0]
    #print(month)
    day = z.split("月")[1].split("日")[0]
    #print(day)
    if int(month) < 10:
        month = '0' + month
    if int(day) <10:
        day = '0' + day
    z = str(datetime.datetime.now().year) + '-' + month + '-' + day
    #print(date)
    return(z)

def time_convert_(z):
    if re.match('\d+分钟前', z):
        minute_0 = re.match('(\d+)', z)
        minute = minute_0.group(0)
        #print(minute)
        z = time.strftime('%Y-%m-%d', time.localtime(time.time() - float(minute) * 60))
        return (z)
        #print(e)
        #print(z)
    elif re.match('\d+小时前', z):
        hour_0 = re.match('(\d+)', z)
        hour = hour_0.group(0)
        z = time.strftime('%Y-%m-%d', time.localtime(time.time() - float(hour) * 60 * 60))
        return(z)
    else:
        z = func(z)
        #print(z)
        return(z)




def crawler_PCI(keyword):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=4000,1600")
    chrome_options.add_argument('disable-javascrip')
    chrome_options.add_argument('disable-images')
    driver = webdriver.Chrome(options=chrome_options)
    url_prefix = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&word=' 
    url = url_prefix + keyword
    driver.get(url)
    for i in range(5):  
        #time.sleep(5)
        try:
            section = driver.find_element_by_xpath('//div[@id = "content_left"]')
            elements = section.find_elements_by_xpath('.//div[@class = "result-op c-container xpath-log new-pmd"]')
        except:
            print('stop in the middle')
            break
        for element in elements:
            title = element.find_element_by_xpath('.//h3[@class = "news-title_1YtI1"]').text
            print(title)
            link_section = element.find_element_by_xpath('.//h3[@class = "news-title_1YtI1"]')
            link = link_section.find_element_by_tag_name('a').get_attribute('href')
            #link = element.find_element_by_xpath('.//h3[@class = "news-title_1YtI1"]').get_attribute('href')
            #print(link)
            time_section = element.find_element_by_xpath('.//div[@class = "news-source"]')
            time_ = time_section.find_element_by_xpath('.//span[@class = "c-color-gray2 c-font-normal"]').text
            #print(time_)
            time_final = time_convert_(time_)
            print(time_final)
            #results = (title, link, time_final)
        next_page_section = driver.find_element_by_xpath('//div[@id = "page"]')
        next_page = next_page_section.find_element_by_link_text("下一页 >").click()
        driver.implicitly_wait(10)
        #time.sleep(5)
    driver.quit()

if __name__ == '__main__':
    keyword = '广州'
    crawler_PCI(keyword)
    