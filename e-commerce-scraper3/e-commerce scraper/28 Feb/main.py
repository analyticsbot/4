import pandas as pd
from babyoye import Babyoye
from fabfurnish import Fabfurnish
from infobeam import Infobeam
from jabong import Jabong
from paytm import Paytm
from pepperfry import Pepperfry
from snapdeal import Snapdeal
from threading import Thread
import time

url1 = 'http://www.babyoye.com/h/Stationary-%26-Writing-Supplies/Blackboard-%26-Whiteboard/Ollington-St.-Collection-Writing-Board-with-Alphabets-Red-Border---Green/p_BP10068108'
url2 = 'http://www.fabfurnish.com/Swayam-Digital-Printed-Shopping-Bag-With-Trendy-Scarf-212108.html'
url3 = 'http://www.infibeam.com/womens-ethnicwear/ishin-womens-semi-chiffon-saree/P-appa-45732317067-cat-z.html'
url4 = 'http://www.jabong.com/sonata-Ocean-Series-Ii-77013Pp03J-Black-Grey-Digital-Watch-361176.html'
url5 = 'https://paytm.com/shop/p/n-a-52-rev-ed-edition-CMPLXBOOKS_9780071781824'
url6 = 'http://www.pepperfry.com/glen-gl-9009-kettle-1202111.html%3Futm_source%3Daff%26utm_medium%3Domg_feed%26utm_campaign%3Domg%26utm_content%3DAppliances'
url7 = 'http://www.snapdeal.com/product/maharaja-whiteline-livo-mixer-grinder/678005968352'

filename = 'urls.xlsx'
xl_file = pd.ExcelFile(filename)
df_urls = xl_file.parse('Sheet1')

bots_run = {'babyoye':False, 'fabfurnish': False, 'infibeam': True, 'pepperfry': False, 'jabong': True,\
            'paytm': False, 'snapdeal': False}

df_babyoye = df_urls.query('Shop == "www.babyoye.com"')
df_fabfurnish = df_urls.query('Shop == "www.fabfurnish.com"')
df_infibeam = df_urls.query('Shop == "www.infibeam.com"')
df_jabong = df_urls.query('Shop == "www.jabong.com"')
df_paytm = df_urls.query('Shop == "www.paytm.com"')
df_pepperfry = df_urls.query('Shop == "www.pepperfry.com"')
df_snapdeal = df_urls.query('Shop == "www.snapdeal.com"')

columns = ['PID', 'URL_raw', 'Title', 'Brand', 'Seller', 'IMG_medium', 'IMG_large', 'Price_mrp', 'Price_selling', 'Price_shipping', 'Delivery', 'COD', 'EMI', 'Category_path', 'Description', 'Offers', 'Average_rating', 'Reviews', 'Status', 'Condition', 'TimeStamp']

df_babyoye_data = pd.DataFrame(columns = columns)
df_fabfurnish_data = pd.DataFrame(columns = columns)
df_infibeam_data = pd.DataFrame(columns = columns)
df_jabong_data = pd.DataFrame(columns = columns)
df_paytm_data = pd.DataFrame(columns = columns)
df_pepperfry_data = pd.DataFrame(columns = columns)
df_snapdeal_data = pd.DataFrame(columns = columns)

def baby_oye(df_data, df_url):
    baby = Babyoye()
    baby.Driver()
    for i, row in df_url.iterrows():
        url = row[2]
        df_data = baby.scrapeData(url, df_data)
    df_data.to_csv('babyoye.csv', index = False, encoding ='utf-8')
    baby.closeDriver()

def fab_furnish(df_data, df_url):
    fab = Fabfurnish()
    fab.Driver()
    for i, row in df_url.iterrows():
        url = row[2]
        df_data = fab.scrapeData(url, df_data)
    df_data.to_csv('fabfurnish.csv', index = False, encoding ='utf-8')
    fab.closeDriver()

def infi_beam(df_data, df_url):
    infi = Infobeam()
    infi.Driver()
    for i, row in df_url.iterrows():
        url = row[2]
        df_data = infi.scrapeData(url, df_data)
    df_data.to_csv('infibeam.csv', index = False, encoding ='utf-8')
    infi.closeDriver()

def jab_ong(df_data, df_url):
    jab = Jabong()
    jab.Driver()
    for i, row in df_url.iterrows():
        url = row[2]
        df_data = jab.scrapeData(url, df_data)
    df_data.to_csv('jabong.csv', index = False, encoding ='utf-8')
    jab.closeDriver()

def pay_tm(df_data, df_url):
    pay = Paytm()
    pay.Driver()
    for i, row in df_url.iterrows():
        url = row[2]
        df_data = pay.scrapeData(url, df_data)
    df_data.to_csv('paytm.csv', index = False, encoding ='utf-8')
    pay.closeDriver()

def pepper_fry(df_data, df_url):
    pepper = Pepperfry()
    pepper.Driver()
    for i, row in df_url.iterrows():
        url = row[2]
        df_data = pepper.scrapeData(url, df_data)
    df_data.to_csv('pepperfry.csv', index = False, encoding ='utf-8')
    pepper.closeDriver()

def snap_deal(df_data, df_url):
    snap = Snapdeal()
    snap.Driver()
    for i, row in df_url.iterrows():
        url = row[2]
        df_data = snap.scrapeData(url, df_data)
    df_data.to_csv('snapdeal.csv', index = False, encoding ='utf-8')
    snap.closeDriver()

threads = []
if bots_run['babyoye']:
    threads.append(Thread(target = baby_oye, name = 'babyoye', args = (df_babyoye_data, df_babyoye)))
if bots_run['fabfurnish']:
    threads.append(Thread(target = fab_furnish, name = 'fabfurnish', args = (df_fabfurnish_data, df_fabfurnish)))
if bots_run['infibeam']:
    threads.append(Thread(target = infi_beam, name = 'infibeam', args = (df_infibeam_data, df_infibeam)))
if bots_run['jabong']:
    threads.append(Thread(target = jab_ong, name = 'jabong', args = (df_jabong_data, df_jabong)))
if bots_run['paytm']:
    threads.append(Thread(target = pay_tm, name = 'paytm', args = (df_paytm_data, df_paytm)))
if bots_run['pepperfry']:
    threads.append(Thread(target = pepper_fry, name = 'pepperfry', args = (df_pepperfry_data, df_pepperfry)))
if bots_run['snapdeal']:
    threads.append(Thread(target = snap_deal, name = 'snapdeal', args = (df_snapdeal_data, df_snapdeal)))

for thread in threads:
    thread.start()
    print 'bot started'
    time.sleep(2)
for thread in threads:
    thread.join()          
