import mechanize, datetime, time, sqlite3, sqlalchemy, re, argparse, logging
from bs4 import BeautifulSoup
from text_unidecode import unidecode
import random,time,sys
import pandas as pd

nickname = 'b3159584'
password = 'facebook'

br = mechanize.Browser()
br.set_handle_robots(False)

br.open('https://fetlife.com/login')
br.select_form(nr=0)
br.form.new_control('text', 'nickname_or_email', {'value': nickname})
br.form.new_control('password', 'password', {'value': password})
resp = br.submit()

df = pd.DataFrame(columns = ['id', 'group_name'])

group_id = 1
while True:
    if group_id % 100==0:
        print group_id
        print df.shape
    
    try:
        url = 'https://fetlife.com/groups/' + str(group_id)
        br.open(url)
        html = br.response().read()
        soup = BeautifulSoup(html)
        group_name = soup.find('h2', attrs = {'class':'group_name bottom'}).getText()
        nrows = df.shape[0]
        df.loc[nrows+1] = [group_id, group_name]
    except:
        pass
    group_id+=1
    time.sleep(random.randint(1,2))

df.to_csv('group_name_mapping.csv', index = False)
        
    
