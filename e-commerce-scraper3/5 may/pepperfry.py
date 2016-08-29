from selenium import websoup
from datetime import datetime
import time, re
from bs4 import BeautifulSoup
import mechanize

class Pepperfry:
    def __init__(self):
        self.name = 'pepperfry'

    def Driver(self):
        self.driver = mechanize.Browser()

    def closeDriver(self):
        self.driver.close()

    def scrapeData(self, url, df):
        driver = self.driver
        driver = mechanize.Browser()
        driver.open(url)
        html = driver.response().read()
        soup = BeautifulSoup(html)

        try:
            attributes = soup.findAll(attrs = {'class':'vip-dtl-desc'})
        except:
            attributes = ''
            
        def getData(element):
            for attribute in attributes:
                if attribute.find('b').getText().strip() == element:
                    return attribute.find('span').getText()
            
        try:
            PID = getData('Sku:')
        except:
            PID = ''
        URL_raw = url
        try:
            Title = soup.find(attrs = {'class':'vip-product-title'}).getText()
        except:
            Title = ''
        try:
            Brand = getData('Brand:')
        except:
            Brand = ''
        try:
            Seller = soup.find(attrs = {'class':'more-from-brand'}).getText().replace('More From ','')
        except:
            Seller = ''
        try:
            IMG_medium = soup.find(attrs = {'id':'vipImage'}).find('img')['src']
        except:
            IMG_medium = ''
        try:
            IMG_large = soup.find_element_by_id('bigImageContainer'})['src']
        except:
            IMG_large = ''
        try:
            Price_mrp = soup.find(attrs = {'class':'vip-prices'}).findAll('li')[0].getText().strip().replace('"','').replace('Retail Price: Rs.','').replace(',','')
            Price_mrp = re.compile(r'(\d+)').search(Price_mrp).group(0)
        except:
            Price_mrp = ''
        try:
            Price_selling = soup.find(attrs = {'class':'vip-prices'}).findAll('li')[1].getText().strip().replace(',','').replace('Offer Price: Rs.','').replace(',','')
        except:
            Price_selling = Price_mrp

        if Price_mrp == '':
            Price_mrp = Price_selling

        try:
            pincode = soup.find(attrs = {'id':'pincode')
            pincode.send_keys('110001')
            soup.find(attrs = {'id':'vipPincodeSub').click()
            time.sleep(3)
        except:
            pass
        try:
            Price_shipping = soup.find(attrs = {'class':'tdcolor1'}).getText()
        except:
            Price_shipping = ''
        try:
            Delivery = soup.find(attrs = {'id':'delivery_status'}).getText()
            if Delivery == '':
                try:
                    Delivery = soup.find(attrs = {'class':'vip-pin-success-txt'}).getText()
                except:
                    Delivery = ''
        except:
            Delivery = ''
        try:
            if soup.find(attrs = {'class':'vip-p-opt-img vip-p-opt-fail'}):
                COD = 'Not Available'
            else:
                COD = 'Available'
        except:
            COD = ''
        try:
            soup.find_element_by_id('emi_strip')
            EMI = 'Available'
        except:
            EMI = ''
        try:
            breadcrums = soup.find(attrs = {'class':'breadcrumb.container'}).findAll('a')[:-1]
            b = ''
            for bread in breadcrums:
                b = b + '|' + bread.getText().strip()
            Category_path = b[1:]
        except:
            Category_path = ''
        try:
            Description = soup.find(attrs = {'class':'other_details_body'}).getText() + soup.find(attrs = {'class':'other_details_panel gb-scroll'}).getText()
        except:
            Description = ''

        try:
            Offers = soup.find(attrs = {'class':'vip-offer-text'}).getText()
        except:
            try:
                Offers = soup.find(attrs = {'class':'vip-cpn-box'}).getText()
            except:
                Offers = ''
        try:
            Average_rating = soup.find(attrs = {'class':'rating-text'}).getText()
        except:
            Average_rating = ''
        Reviews = ''
        try:
            if 'THIS ITEM IS SOLD OUT!' not in str(soup):
                Status = 'OUT OF STOCK'
            else:
                Status = 'IN STOCK'
        except:
            Status = 'IN STOCK'

        Condition = 'NEW'
        TimeStamp = str(datetime.now())

        nrow = df.shape[0]
        df.loc[nrow+1] = [PID, URL_raw, Title, Brand,Seller, IMG_medium, IMG_large, Price_mrp, Price_selling, Price_shipping, Delivery,\
                          COD,EMI, Category_path,Description,Offers,Average_rating,Reviews,Status,Condition,TimeStamp]

        return df
