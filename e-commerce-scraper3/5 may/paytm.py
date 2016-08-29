from selenium import websoup
from datetime import datetime
import time, re
from bs4 import BeautifulSoup
import mechanize

class Paytm:
    def __init__(self):
        self.name = 'paytm'

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


        attributes = soup.findAll(attrs = {'class':'attributes')
        def getData(element):
            for attribute in attributes:
                if attribute.find(attrs = {'class':'col1').text == element:
                    return attribute.find(attrs = {'class':'col2').text

        
            
        try:
            PID = getData('Product Code')
        except:
            PID = ''
        URL_raw = url
        try:
            Title = soup.find(attrs = {'class':'img-description'}).find_element_by_tag_name('h1').text
        except:
            Title = ''
        try:
            Brand = getData('Brand')
        except:
            Brand = ''
        try:
            Seller = soup.find(attrs = {'class':'profile-description'}).text.split('\n')[1]
        except:
            Seller = ''
        try:
            IMG_medium = soup.find(attrs = {'class':'img-dis'}).find('img')['src']
        except:
            IMG_medium = ''
        try:
            IMG_large = soup.find(attrs = {'class':'img-dis').find('img')['ng-src']
        except:
            IMG_large = ''
        try:
            Price_mrp = soup.find(attrs = {'class':'md-raised fl md-button md-default-theme').find('span')\
                        .text.strip().replace('"','').split('|')[0].replace('Buy for Rs ','').replace(',','').split('\n')[1].replace('Rs.','')
        except:
            Price_mrp = ''
        try:
            Price_selling = soup.find(attrs = {'class':'md-raised fl md-button md-default-theme').find('span')\
                            .text.strip().replace('"','').split('|')[0].replace('Rs. ','').replace(',','').replace('Buy for Rs ','').split('\n')[0]
        except:
            Price_selling = Price_mrp

        if Price_mrp == '':
           Price_mrp =  Price_selling
        try:
            zipcode = soup.find(attrs = {'class':'ng-pristine.ng-valid.md-input.ng-valid-maxlength.ng-touched'})
            zipcode.send_keys('110001')
            soup.find(attrs = {'class':'apply').click()
        except:
            pass
        time.sleep(1)
        try:
            data = soup.find(attrs = {'class':'detail-Shipp.dotted-border'}).findAll('li')
        except:
            data = ''
        Price_shipping = ''
        try:
            for d in data:
                if 'Shipping Charges' in d.text:
                    Price_shipping = d.text.replace('Shipping Charges: Rs','')
                elif 'Shipping : Free' in d.text:
                    Price_shipping = 0
                else:
                    Price_shipping = ''
        except:
            Price_shipping = ''
        Delivery = 'Not Available'

        try:
            for d in data:
                if 'Delivery available' in d.text:
                    Delivery = 'Available'
                elif 'Delivery not available' in d.text:
                    Delivery = 'Not Available'
                else:
                    Delivery = 'Not Available'
        except:
            Delivery = 'Not Available'
        COD = ''
        try:
            for d in data:
                if 'Cash on Delivery available' in d.text:
                    COD = 'Available'
                elif 'Cash on Delivery not available' in d.text:
                    COD = 'Not Available'
                else:
                    COD = ''
        except:
            COD = 'Not Available'
        try:
            EMI = ''
        except:
            EMI = ''
        try:
            breadcrums = soup.find(attrs = {'class':'breadcrum'}).findAll('a')
            b = ''
            for bread in breadcrums:
                b = b + '|' + bread.text.strip()
            Category_path = b[1:]
        except:
            Category_path = ''
        try:
            Description = soup.find(attrs = {'class':'ProductDescription'}).text
        except:
            Description = ''
        try:
            Offers = soup.find(attrs = {'class':'offer-cont'}).text
        except:
            Offers = ''
        try:
            Average_rating = soup.find(attrs = {'class':'rating-text'}).text.replace('/5','').replace('ratings','')
        except:
            Average_rating = ''
        Reviews = ''
        try:
            if soup.find(attrs = {'class':'md-raised fl md-button md-default-theme'}).find('span').text.strip():
                Status = 'IN STOCK'
            else:
                Status = 'OUT OF STOCK'
            if 'Out of stock' in soup.page_source:
                Status = 'OUT OF STOCK'
            else:
                Status = 'IN STOCK'
        except:
            if 'Out of stock' in soup.page_source:
                Status = 'OUT OF STOCK'
            else:
                Status = 'IN STOCK'

        Condition = 'NEW'
        TimeStamp = str(datetime.now())

        nrow = df.shape[0]
        df.loc[nrow+1] = [PID, URL_raw, Title, Brand,Seller, IMG_medium, IMG_large, Price_mrp, Price_selling, Price_shipping, Delivery,\
                          COD,EMI, Category_path,Description,Offers,Average_rating,Reviews,Status,Condition,TimeStamp]

        return df
