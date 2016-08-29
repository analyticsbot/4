from selenium import websoup
from datetime import datetime
import time, re
from bs4 import BeautifulSoup
import mechanize

class Snapdeal:
    def __init__(self):
        self.name = 'snapdeal'

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
            soup.find(attrs = {'class':'sd-icon sd-icon-delete-sign'}).click()
        except:
            pass
        attributes = soup.findAll(attrs = {'class':'linear_list'})
        def getData(element):
            for attribute in attributes:
                if attribute.find(attrs = {'class':'col1'}) .getText() == element:
                    return attribute.find(attrs = {'class':'col2'}) .getText()
            
        PID = url.split('/')[-1]
        URL_raw = url
        try:
            Title = soup.find(attrs = {'class':'pdp-e-i-head'}) .getText()
        except:
            Title = ''
        try:
            Brand = soup.find(attrs = {'class':'pdp-e-brand-logo-img'}).find_element_by_tag_name('img').get_attribute('alt')
        except:
            Brand = ''
        try:
            Seller = soup.find(attrs = {'class':'pdp-e-seller-info-name reset-margin'}) .getText()
        except:
            Seller = ''
        try:
            IMG_medium = soup.find(attrs = {'id':'bx-slider-left-image-panel'}).find_element_by_tag_name('img').get_attribute('src')
        except:
            IMG_medium = ''
        try:
            IMG_large = soup.find(attrs = {'id':'bx-slider-left-image-panel'}).find_element_by_tag_name('img').get_attribute('bigsrc')
        except:
            IMG_large = ''
        try:
            Price_mrp = soup.find(attrs = {'class':'pdpCutPrice'}) .getText().strip().replace('"','').replace(',','').replace('Rs.','').strip()
        except:
            Price_mrp = ''
        try:
            Price_selling = soup.find(attrs = {'class':'payBlkBig') .getText().strip().replace(',','')
        except:
            Price_selling = Price_mrp

        if Price_mrp == '':
            Price_mrp = Price_selling

        try:
            pincode = soup.find(attrs = {'id':'pincode-check')
            pincode.send_keys('110001')
            soup.find_element_by_id('pincode-check-bttn').click()
            time.sleep(2)
        except:
            pass
        try:
            Price_shipping = soup.find(attrs = {'class':'freeDeliveryChargeCls'}) .getText()
            if 'Free' in Price_shipping:
                Price_shipping = 0
            elif 'Delivery' in Price_shipping:
                Price_shipping = re.findall(r'\d+',Price_shipping.replace(', Delivery Charges : +Rs',''))[0]
        except:
            try:
                Price_shipping = soup.find(attrs = {'class':'freeDeliveryChargeCls freeDeliveryCharge'}) .getText()
                if 'Free' in Price_shipping:
                    Price_shipping = 0
                elif 'Delivery' in Price_shipping:
                    Price_shipping = re.findall(r'\d+',Price_shipping.replace(', Delivery Charges : +Rs',''))[0]
            except:
                try:
                    Price_shipping = soup.find(attrs = {'class':'rsInfo.addPrice.delivery-charges'}) .getText()
                    if 'Free' in Price_shipping:
                        Price_shipping = 0
                    elif 'Delivery' in Price_shipping:
                        Price_shipping = re.findall(r'\d+',Price_shipping.replace(', Delivery Charges : +Rs',''))[0]
                except:
                    Price_shipping = ''
        try:
            Delivery = soup.find(attrs = {'class':'otoDRange'}) .getText()
            Delivery = re.findall(r'\d+\s-\s\d+\sday', Delivery)[0]
        except:
            Delivery = ''
        try:
            soup.find(attrs = {'id':'pincode-cod'})
            COD = 'Available'
        except:
            COD = 'Not Available'
        try:
            soup.find(attrs = {'class':'pdp-emi'})
            EMI = 'Available'
        except:
            EMI = 'Not Available'
        try:
            breadcrums = soup.find(attrs = {'class':'bread-crumb'}).findAll('a')
            b = ''
            for bread in breadcrums:
                b = b + '|' + bread .getText().strip()
            Category_path = b[1:]
        except:
            Category_path = ''
        try:
            Description = soup.find(attrs = {'id':'productSpecs'}) .getText()
        except:
            Description = ''

        try:
            Offers = soup.find(attrs = {'class':'row.pdp-e-i-alloffers'}) .getText().split('\n')[0]
        except:
            Offers = ''
        try:
            Average_rating = soup.find(attrs = {'class':'product_review'}).find('span') .getText()
            try:
                Num_Review = soup.find(attrs = {'class':'review_land js-jl-omni js-pdp-nav-sec'}) .getText().replace('Reviews','').strip()
            except:
                Num_Review = ''
            Average_rating = Average_rating + '(' + Num_Review+')'
            
        except:
            Average_rating = ''
        try:
            Reviews = ''
            reviews = soup.findAll(attrs = {'class':'commentlist first jsUserAction'})[:10]
            for review in reviews:
                author = review.find(attrs = {'class':'_reviewUserName'}) .getText()
                date = review.find(attrs = {'class':'date.LTgray'}) .getText()
                description = review.find('p') .getText().replace('\n','')
                Reviews += str({'author':author, 'date':date, 'description':description}) + "; "
            Reviews = Reviews[:-1]
        except:
            Reviews = ''
        try:
            if soup.find(attrs = {'class':'intialtext'}) .getText().strip()=='BUY NOW':
                Status = 'IN STOCK'
            else:
                Status = 'OUT OF STOCK'
        except:
            Status = 'OUT OF STOCK'

        Condition = 'NEW'
        TimeStamp = str(datetime.now())

        nrow = df.shape[0]
        df.loc[nrow+1] = [PID, URL_raw, Title, Brand,Seller, IMG_medium, IMG_large, Price_mrp, Price_selling, Price_shipping, Delivery,\
                          COD,EMI, Category_path,Description,Offers,Average_rating,Reviews,Status,Condition,TimeStamp]

        return df
