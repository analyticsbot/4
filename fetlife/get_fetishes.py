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

df = pd.DataFrame(columns = ['id', 'fetish'])

fet_id = 1
while True:
    if fet_id % 100==0:
        print fet_id
        print df.shape
    
    try:
        url = 'https://fetlife.com/fetishes/' + str(fet_id)
        br.open(url)
        html = br.response().read()
        soup = BeautifulSoup(html)
        fetish = soup.find('h2', attrs = {'class':'mbn'}).getText()
        nrows = df.shape[0]
        df.loc[nrows+1] = [fet_id, fetish]
    except:
        pass
    fet_id+=1
    time.sleep(random.randint(1,2))

df.to_csv('fetish_mapping.csv', index = False)
        
    
