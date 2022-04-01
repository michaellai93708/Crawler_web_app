from urllib.request import urlopen, urljoin 
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
import re
import requests as req
import datetime
import time
import mysql
import mysql.connector

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-tw',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15',
    'Connection': 'keep-alive',
    'Referer': 'http://s.wanfangdata.com.cn/paper?q=%E6%99%BA%E6%85%A7%E5%9F%8E%E5%B8%82'
}
cookies = {'cookie':'JSESSIONID=AB3AE2C67A8127DF4BC91870D67D0DAE;\
Hm_lpvt_838fbc4154ad87515435bf1e10023fab=1605842089; Hm_lvt_838fbc4154ad87515435bf1e10023fab=1605497522,1605576911,1605753755,1605838615;\
SEARCHHISTORY_0=UEsDBBQACAgIANhZdFEAAAAAAAAAAAAAAAABAAAAMO2a7W%2FbRBzH%2FxUUyX1VdXdn352vUjQla7o%2B%0A0qc0SYt4cU2cxKsTO2e7aYqQBoK1KmKiQoCAiiEkVvGCCmlvNsTgj6HJyn%2F\
BeS2q1sVeM0KW0EiR%0AfGfHPvnzvd%2F9Hs7vvBfz%2BIZlvM0rRmy86lvWaMwsxMZj5QlVrBp4h6gsNhrzXUNMF%2F75g2twkS%2Bn%0AG468BcqLwgpu8Dxn%2FMYNd6zOq0VeLRW4x8fydmUsX73hcMcQN2txBQElRRU9pehJJUW\
UpKokJ5QU%0AVhLyDJXjGNuOMFzXtKvyiW89u%2F9J69HT5vGuvOI9Hy3WOnzQ3Nv%2F8%2B4HzZ8fnjz9VDZOfvvm9Pg4%0AaDz%2BvLn3k2w8Ozpo7d9t7f%2FYPNi%2F6O591vruUHZb3%2B82d%2B8FjUdfnB59FDzq8JfWl0%2Baf3wl\
26dH%0A9%2F764SA4%2Be3vJ08eyoGrfmXS9qvy5YkORmN5YXDPSJsBLkgA1jVAqCYpvT8ahrK24%2BXLt3eYpoIu%0AopT4GFOSiaChS4I04MgmA7iykdQVHV0G2vr619bHR80H95uPP%2BwPpBgCiNtAVRnUgOQVDjU7NWEV%0AK0VMgDaEe\
kWoOiVM8gqHemduYxPwEkWqOjT6KKNXdYKYpBSOcoonKwXiVAjsiGS9Xm%2FH8uyW88Oc%0A6XpjBfvmxXPikrRpj7hlu%2F68O%2BLwkrFi7hhxBEbO%2Fpa1RaHr8%2FsFUiqi7VhRQqFKAIHhrNSsA7aT%0A9XnESF%2FDGjHdtDBLJUOkeS\
neHlQ0IqIxhNozAqp8%2FXBG8%2FVGeQnvzFCKe8GIW9YFoYLhcdMK53R5%0ACkVz6qelUsUMIqy9rAghOtWAhB2xWFp4IXcnO01h7xTpzJQjFTTdKdOLnx1Wq0GzyrdWXhyvaArX%0AS%2Fhe2RbxIrdcYyRvC2MxsJ%2FzPrckuEIj6TeWDdf2\
Rd44vyDk6xmLXEhqIZbST%2FNAQzqmbWcBUFUp%0AcPgscCYalTReTmmos%2BCuG3Z5oed%2Fucj3mSJUg7qEHREZMuC4%2FrzPNH2oSE8UURGQsMMVqeZEJjeb%0Aq6m4J%2F79Soq8in8%2FkQ%2F3UgjojEmsEXGoSE3O2LlpqneWJw2t4bWsA\
esyCtYl7HBFtrd8191MZXAP%0A44Z%2Fr8hVYt9B0EfmKITgKI9eWtNEsgEhGSj%2FMXj6SDt5WR%2BNUYwD9BERV8mYTGYSNQY6q0wO9emC%0APhgiBIhEH66Pn2BwfW51AVE0QPoMgiJhHkf%2BJOxwRWACZNwZsiHF6xtF%2FhfxlwSvIyixRnj\
7teza%0AbCG7hVBPCoHXhz1BEFK5GkXUFe3lur0Ilwhhg%2BTJB3YlCjJBVTqHCN%2B9CLant3xQ1MiwWtIbRQhA%0AEna4ImBJrNf5Zhr2LpgaFjF7XcTEGgUwImTLrFj%2B%2Bm3qEtSTWXBpA%2BZV2wtvYs%2BK6JBJGuHIbpVy%0AiwmnyjS1v\
zf4urxLhYIXDqfCZ9bzAt4qM9aTalMXtz1fPz%2B74iYogkRSCUc37fDyXKbTosP1%2FpwB%0AUwAioo3UUnpWLKw6pLO0p0OmV7OwN%2BQSCFZB2w8YGEAUkIjEpVSbrWW2K3IV7KxMeZ1nJMOazEsi%0AaotTmxsbExXBO83ErzFULdjjCFLsd%2F8\
GUEsHCJF5lbemBAAArCgAAA%3D%3D%0A; zh_choose=t; firstvisit_backurl=http%3A//www.wanfangdata.com.cn'}

mysql_connection = mysql.connector.connect(user = 'root', password = 'Laijiachong1', host = 'localhost',database = 'crawler' )

cursor = mysql_connection.cursor()
sql_insert = "INSERT INTO results_1 (Title, Link, Author, Tag, Date) VALUES (%s, %s, %s, %s, %s)"

def input_search_word():
    key_word = input('search word:')
    return key_word

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

def crawler_wanfang():
    url_prefix = 'http://www.wanfangdata.com.cn/search/searchList.do?searchType=all&showType=&pageSize=&searchWord=' 
    url = url_prefix + '智慧城市'
    #input_search_word()
    website = req.get(url,cookies = cookies, headers = headers)
    soup = BeautifulSoup(website.text, 'lxml')
    print(soup)
    #OBTAINING WEBSITE AND CONVERTING INTO PYTHON READABLE FILE
    div_result_lists = soup.find_all('div', {'class': 'ResultList'})
    #print(div_result_lists)
    for result_list in div_result_lists:
        titles_section = result_list.find('div', {'class': 'title'})
        titles_a = titles_section.find('a')
        title = titles_a.get_text()
        #print(title)
        # TITLE SECTION 

        links_section = result_list.find('div', {'class': 'title'})
        links_a = links_section.find('i')
        link = links_a['onclick']
        match = re.search("this.id,'(.*?)','(.*)'", link)
        id_ = match.group(1)
        type_ = match.group(2)
        category = type_analysis(type_)
        link_ = 'http://d.wanfangdata.com.cn/'+ category +'/' + id_
        #print(link_)
        # LINK SECTION

        authors_section = result_list.find('div', {'class': 'author'})
        authors_a = authors_section.find_all('a')
        author_list = []
        for author_a in authors_a:
            author = author_a.get_text()
            author_list.append(author)
            author_list_final = (', '.join(str(x) for x in author_list))
        #print(author_list_final)
        # AUTHOR SECTION

        tags_section = result_list.find('div', {'class': 'Keyword'})
        if tags_section == None:
            continue
        tags_a = tags_section.find_all('a')
        tag_list = []
        for tag_a in tags_a:
            tag = tag_a.get_text()
            tag_list.append(tag)
            tag_list_final = (', '.join(str(x) for x in tag_list))
        #print(tag_list_final)
        # TAG SECTION
        
        date_section = result_list.find('div', {'class': 'Volume'})
        
        #date_a = date_section.find_all('a')
        #print(date_a)
        date = date_section.get_text()
        date_final = " ".join(date.split())
        #print(date_final)
        # DATE SECTION

        results = (title, link_, author_list_final, tag_list_final, date_final)
        #print(results)
        cursor.execute(sql_insert,results)
        mysql_connection.commit()

if __name__ == '__main__':
    crawler_wanfang()
