from urllib.request import urlopen, urljoin 
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
import re
import requests as req
import datetime
import time
import mysql
import mysql.connector
import threading 

mysql_connection = mysql.connector.connect(user = 'root', password = 'Laijiachong1', host = 'localhost',database = 'crawler' )

cursor = mysql_connection.cursor()
sched = BlockingScheduler()


def func(z):
    month = z.split("月")[0]
    day = z.split("月")[1].split("日")[0]
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

def time_convert_iyiou(z):
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
        return(z)
        
def crawler_leiphone():
    url = 'https://www.leiphone.com/category/ai'
    #url = 'https://www.leiphone.com/category/ai/page/[1]'
    website = req.get(url)
    soup = BeautifulSoup(website.text, 'lxml')
    #OBTAINING WEBSITE AND CONVERTING INTO PYTHON READABLE FILE
    sql_insert = "INSERT INTO app_result_b (Title, Link, Author, Tag, Time) VALUES (%s, %s, %s, %s, %s)"
    
    #IMPORTING ALL NECESSARY PACAKGES
    div_total = soup.find_all('div', {'class':'box'})
    for div in div_total:
        div_links = div.find('h3')
        #THIS FOR LOOP IS USED TO FIND ALL SECTION THAT HAS 'H3' UNDER DIVISION WITH CLASS'BOX'            if div_links == None:
        if div_links == None:
            break
        #CHECK IF ALL THE 'H3'SECTIONS WERE FOUND
        all_links = div_links.find_all('a',{'class':'headTit'}, {'href':re.compile('www.leiphone.com/news')})
        #FIND LINK THAT ARE UNDER THE NEWS SECTION
        div_titles = div.find('h3')
        all_titles = div_titles.find_all('a',{'class':'headTit'},'title')
        #FIND THE TITLE OF THE LINK FOUND IN THE PREVIOUS CODE 
        div_authors = div.find('div', {'class':'msg clr'})
        all_authors = div_authors.find_all('a', {'class':'aut'}, 'href')
        #FIND THE AUTHOR OF THE LINK FOUND 
        div_tag = div.find('div', {'class':'tags'})
        all_tags = div_tag.find_all('a', {'target':'_blank'}, 'title')
        #FIND THE TAG/TAGS OF THE LINK FOUND
        div_time = div.find('div', {'class':'msg clr'})
        all_times = div_time.find_all('div',{'class': 'time'} )
        #FIND THE TIME OF ALL LINK FOUND 
        tag = []
       
       
        for link in all_links:
            a = (link['href'])
            #print(link['href'])
            #return ALL THE LINK/LINKS FOUND
            a_hash = (hash(a))
        for titles in all_titles:
            b = (titles['title'])
            #print(titles['title'])
            #return ALL THE TITLE FOUND
        for authors in all_authors:
            c = (authors.get_text())
            #print(authors['href'])
            #return ALL THE AUTHOR FOUND
        for tags in all_tags:
            tag.append(tags['title'])
            d = (', '.join(str(x) for x in tag))
            #print(tags['title'])
            #return ALL THE TAGS FOUND
        for times in all_times:
            e = (times.get_text())
            #return ALL TIMES FOUND
            e = time_convert_leiphone(e)
        #print(e)
        results = (b, a, c, d, e)
        cursor.execute(sql_insert,results)
        mysql_connection.commit()
        
    
    #print('this is page', i)
    #print(check_repeat)

def crawler_iyiou():
    url = 'https://legacy.iyiou.com/smartcity/'
    #url = 'https://www.leiphone.com/category/ai/page/[1]'
    website = req.get(url)
    soup = BeautifulSoup(website.text, 'lxml')
    #OBTAINING WEBSITE AND CONVERTING INTO PYTHON READABLE FILE
    sql_insert = "INSERT INTO app_result_b (Title, Link, Author, Tag, Time) VALUES (%s, %s, %s, %s, %s)"
   
    li_total = soup.find_all('li', {'class':'clearFix thinkTankTag'})
    #FIND ANY DIVISION THAT HAS A CLASS 'clearFix thinkTankTag'
    for li in li_total:
        div_links = li.find('div', {'class':'text fl'})
        #THIS FOR LOOP IS USED TO FIND ALL SECTION THAT HAS 'H3' UNDER DIVISION WITH CLASS'BOX'            if div_links == None:
        if div_links == None:
            break
        #CHECK IF ALL THE 'H3'SECTIONS WERE FOUND
        all_links = div_links.find_all('a',{'href':re.compile('https://legacy.iyiou.com/[^author]')})
        #FIND LINK THAT ARE UNDER THE NEWS SECTION
        div_titles = li.find('div', {'class':'text fl'})
        all_titles = div_titles.find_all('h2')
        #FIND THE TITLE OF THE LINK FOUND IN THE PREVIOUS CODE 
        div_authors = li.find('div', {'class':'fl typeName'})
        all_authors = div_authors.find_all('span')
        #FIND THE AUTHOR OF THE LINK FOUND 
        div_tag = li.find('div', {'class':'box-lables1 clearFix'})
        all_tags = div_tag.find_all('span', {'class':'tag_content'})
        #FIND THE TAG/TAGS OF THE LINK FOUND
        div_time = li.find('div', {'class':'box-lables clearFix'})
        all_times = div_time.find_all('div',{'class': 'time'} )
        #FIND THE TIME OF ALL LINK FOUND 
        tag = []
        
       
        for link in all_links:
            a = (link['href'])
            #print(link['href'])
            #return ALL THE LINK/LINKS FOUND
            a_hash = (hash(a))
        for titles in all_titles:
            b = (titles.get_text())
            #print(titles['title'])
            #return ALL THE TITLE FOUND
        for authors in all_authors:
            c = (authors.get_text())
            #print(authors['href'])
            #return ALL THE AUTHOR FOUND
        for tags in all_tags:
            tag.append(tags.get_text())
            d = (', '.join(str(x) for x in tag))
            #print(tags['title'])
            #return ALL THE TAGS FOUND
        for times in all_times:
            e = (times.get_text())
            #return ALL TIMES FOUND
            e = time_convert_iyiou(e)
        #print(e)
        results = (b, a, c, d, e)
        cursor.execute(sql_insert,results)
        mysql_connection.commit()
        
    
    #print('this is page', i)
    #print(check_repeat)

threads = []
t1 = threading.Thread(target=crawler_leiphone)
threads.append(t1)
t2 = threading.Thread(target=crawler_iyiou)
threads.append(t2)

def schedule_job():
    sched.add_job(crawler_leiphone, 'cron', day_of_week = 'mon-fri',hour = '0')
    sched.add_job(crawler_iyiou, 'cron', day_of_week = 'mon-fri',hour = '0')
    #sched.add_job(crawler_leiphone, 'interval', seconds = 10)
    #sched.add_job(crawler_iyiou, 'interval', seconds = 10)
    sched.start()

def threading_schedule_job():
    thread = threading.Thread(target=schedule_job)
    thread.start()
    print('Last update at', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

if __name__ == '__main__':
    cursor.execute("DELETE FROM app_result_b")
    mysql_connection.commit()
    for t in threads:
        t.start() 
    print('Last update at', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    threading_schedule_job()
#THESE LINES WERE ADDED IN ORDER TO START THE PROGRAM AT TIME T=0, AKA WHEN CLICK RUN
#SOMEHOW IN VSCODE THIS TWO LINES MUST BE ADDED SIMPLILY CALLING THE FUNCTION WON'T WORK


    
    
    
#THIS WHILE LOOP WAS USED TO ENSURE THIS CRAWLER WOULD RUN EVERY DAY AT 12AM, MONDAY TO FRIDAY