from urllib.request import urlopen, urljoin 
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
import re
import requests as req
import datetime
import mysql
import mysql.connector

mysql_connection = mysql.connector.connect(user = 'root', password = 'Laijiachong1', host = 'localhost',database = 'crawler' )
cursor = mysql_connection.cursor()
sql_insert = "INSERT INTO app_result_b (Title, Link, Author, Tag, Time) VALUES (%s, %s, %s, %s, %s)"

url = 'https://zhidx.com/p/category/人工智能'
website = req.get(url)
soup = BeautifulSoup(website.text, 'lxml')
#print(soup)
all_li = soup.find_all('li')
#print(all_li)
# TITLE LINK AUTHOR TAG TIME
cursor.execute("DELETE FROM app_result_b")
mysql_connection.commit()
for li in all_li:
    try:
        title = li.find('div',{'class': 'info-left-title'}).text
        #print(title)
        title = title.replace('\n', '')
    except:
        title = None
        continue
    try:
        div = li.find('div',{'class': 'info-left-title'})
        a = div.find('a')
        link = a['href']
        #print(link)
    except:
        link = None
        continue
    try:
        large_div = li.find('div',{'class': 'info-left-related'})
        author = large_div.find('div',{'class': 'ilr-author-name'}).text
        #print(author)
    except:
        author = None
        continue
    
    large_div = li.find('div',{'class': 'info-left-related'})
    time_ = large_div.find('div',{'class': 'ilr-time'}).text
    time = str(datetime.datetime.now().year) + '-' + str(time_)
    time = time.replace('\n', '').replace(' ', '')
    #print(time)
    tag = 'DNE'
    results = (title, link, author, tag, time)
    print(results)
    
    cursor.execute(sql_insert,results)
    mysql_connection.commit()




   