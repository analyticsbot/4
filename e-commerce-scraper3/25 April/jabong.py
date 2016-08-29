from selenium import websoup
from datetime import datetime
import time, re
from bs4 import BeautifulSoup
import mechanize

class Jabong:
    def __init__(self):
        self.name = 'jabong'

    def soup(self):
        self.driver = mechanize.Browser()

    def closesoup(self):
        self.driver.close()

    def scrapeData(self, url, df):
        
        driver = self.driver
        driver = mechanize.Browser()
        driver.open(url)
        html = driver.response().read()
        soup = BeautifulSoup(html)
        
        try:
            product_details = soup.find(attrs = {'class':'prod-main-wrapper'}).findAll('li')
            
            def getElement(element):
                for product_detail in product_details:
                    name = product_detail.find('label').getText().strip()
                    if name == element:
                        return product_detail.find('span').getText().strip()
        except:
            pass
        try:
            PID = getElement('SKU')
        except:
            PID = ''
        URL_raw = url
        try:
            Title = soup.find(attrs = {'class':'product-title'}).getText()
        except:
            Title = ''
        try:
            Brand = soup.find(attrs = {'class':'brand'}).getText()
        except:
            Brand = ''
        Seller = ''
        try:
            IMG_medium = soup.find(attrs = {'class':'slide slick-slide'}).find('img')['src']
        except:
            IMG_medium = ''
        try:
            soup.find(attrs = {'class':'slide slick-slide slick-active'}).click()
            time.sleep(1)
            IMG_large = soup.find(attrs = {'class':'slide slick-slide slick-active'}).find('img')['src']
        except:
            IMG_large = ''
        try:
            Price_mrp = soup.find(attrs = {'class':'standard-price'}).getText().strip().replace('"','')
        except:
            Price_mrp = ''
        try:
            Price_selling = soup.find(attrs = {'class':'actual-price'}).getText().strip().replace('"','')
        except:
            Price_selling = Price_mrp

        print Price_mrp, Price_selling

        if Price_mrp == '':
            Price_mrp = Price_selling

        Price_shipping = ''
        try:
            Delivery = soup.find(attrs = {'id':'pdp-tat-tool-tip'}).getText().split('|')[0].replace('Delivery in','')
        except:
            Delivery = ''
        try:
            COD = soup.find(attrs = {'id':'pdp-tat-tool-tip'}).getText().split('|')[1].strip().replace('cod','')
        except:
            COD = ''
        EMI = ''
        try:
            breadcrums = soup.find(attrs = {'class':'breadcrumb'}).findAll('a')
            b = ''
            for bread in breadcrums:
                b = b + '|' + bread.getText().strip()
            Category_path = b[1:]
            #Category_path = re.sub( '\|+', ' ', Category_path ).strip()
        except:
            Category_path = ''
        try:
            Description = soup.find(attrs = {'class':'prod-info'}).getText()
        except:
            Description = ''
        Offers = ''
        try:
            Average_rating = soup.find(attrs = {'class':'current-rating'}).getText()
        except:
            Average_rating = ''
        try:
            Reviews = ''
            reviews = soup.findAll(attrs = {'class':'review-wrapper clearfix'})
            for review in reviews:
                author = review.find('b').getText()
                date = review.find(attrs = {'class':'rating-timeline'}).getText()
                description = review.find(attrs = {'class':'user-comment col-md-9 col-sm-8 col-xs-12'}).getText()
                Reviews += str({'author':author, 'date':date, 'description':description}) + "; "
            Reviews = Reviews[:-1]
        except:
            Reviews = ''
        try:
            soup.find(attrs = {'class':'sold-product'})
            Status = 'OUT OF STOCK'
        except:
            Status = 'IN STOCK'
        Condition = 'NEW'
        TimeStamp = str(datetime.now())


        nrow = df.shape[0]
        df.loc[nrow+1] = [PID, URL_raw, Title, Brand,Seller, IMG_medium, IMG_large, Price_mrp, Price_selling, Price_shipping, Delivery,\
                          COD,EMI, Category_path,Description,Offers,Average_rating,Reviews,Status,Condition,TimeStamp]

        return df
