from urllib.request import urlopen, urljoin 
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import re
import requests as req
import datetime
import time
import mysql
import mysql.connector
import threading 
def func(z):
    month = z.split("月")[0]
    day = z.split("月")[1].split("日")[0]
    if int(month) >= 10:
        current_year = int(datetime.datetime.now().year) - 1
        z = str(current_year) + '-' + month + '-' + day
    else:
        z = str(datetime.datetime.now().year) + '-' + month + '-' + day
    #print(date)
    return(z)

def time_convert_leiphone(z):
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
    elif re.match('昨天', z):
        #ytd_0 = re.match('%H:%M)', z)
        #print(ytd_0)
        z = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 60 * 60))
        return(z)
    elif re.match('前天', z):
        #ytd_0 = re.match('%H:%M)', z)
        #print(ytd_0)
        z = time.strftime('%Y-%m-%d', time.localtime(time.time() - 2 * 24 * 60 * 60))
        return(z)
    elif re.match('\d+天前', z):
        day_0 = re.match('(\d+)', z)
        day = day_0.group(0)
        z = time.strftime('%Y-%m-%d', time.localtime(time.time() - float(day) * 24 * 60 * 60))
        return(z)
    else:
        z = func(z)
        #print(z)
        return(z)

def crawler_leiphone_smart_city():
    url = 'https://www.leiphone.com/category/smartcity'
    website = req.get(url)
    soup = BeautifulSoup(website.text, 'lxml')
    #OBTAINING WEBSITE AND CONVERTING INTO PYTHON READABLE FILE
    sql_insert = "INSERT INTO app_result_b (Title, Link, Author, Tag, Time) VALUES (%s, %s, %s, %s, %s)"
    #print(soup)
    all_ = soup.find('ul', {'class':'clr'})
    all_div = all_.find_all('div', {'class':'box'})
    for div in all_div:
        title_and_link_section = div.find('h3')
        title = title_and_link_section.text
        title = ' '.join(title.split())
        #print(title)
        link_section = title_and_link_section.find('a')
        link = link_section['href']
        #print(link)
        author_time_and_tag_section = div.find('div', {'class':'msg clr'})
        author = author_time_and_tag_section.find('a').text
        author = ''.join(author.split())
        #print(author)
        tag = author_time_and_tag_section.find('div', {'class':'tags'}).text
        tag = ''.join(tag.split())
        #print(tag)
        time_initial = author_time_and_tag_section.find('div', {'class': 'time'}).text
        time = time_convert_leiphone(time_initial)
        #print(time)
        results = (title, link, author, tag, time)
        print(results)

if __name__ == '__main__':
    crawler_leiphone()