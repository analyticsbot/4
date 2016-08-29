from datetime import datetime
import time
from selenium.webdriver.common.keys import Keys
import mechanize
from bs4 import BeautifulSoup
import requests

class Fabfurnish:
    def __init__(self):
        self.name = 'fabfurnish'

    def Driver(self):
        pass

    def closeDriver(self):
        pass

    def scrapeData(self, url, df):
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content)

        try:
            PID = soup.find(attrs = {'class':'prd_attr_desc prd_attr_desc_wd'}).getText()
        except:
            PID = ''
        URL_raw = url
        try:
            Title = soup.find(attrs = {'class':'prd-title-new'}).getText()
        except:
            Title = ''
        try:
            Brand = Title.split()[0]
        except:
            Brand = ''
        Seller = ''
        try:
            IMG_medium = soup.find(attrs = {'id':'imgThumb_1'}).find('a')['href']
        except:
            IMG_medium = ''
        try:
            IMG_large = soup.find(attrs = {'id':'imgThumb_1'}).find('img')['longdesc']
        except:
            IMG_large = ''
        try:
            Price_mrp = soup.find(attrs = {'id':'price_box'}).getText().strip().replace(',','')
        except:
            Price_mrp = ''
        try:
            Price_selling = soup.find(attrs = {'id':'special_price_box'}).getText().strip().replace(',','')
        except:
            Price_selling = Price_mrp

        if Price_mrp == '':
            Price_mrp = Price_selling
            
        try:
            Price_shipping = soup.find(attrs = {'id':'product-ship-charges'}).getText()
            if Price_shipping == None:
                Price_shipping = ''
        except:
            Price_shipping = ''
        try:
            variationSkuSimple = soup.find('input', attrs = {'id':'variationSkuSimple'})['value']
            url = 'http://www.fabfurnish.com/catalog/deliverydetails/delivery/110001/sku/' + variationSkuSimple
            r = requests.get(url)
            data = dict(eval(r.content))
            try:
                COD = data['cod_message']
            except:
                COD = ''

            try:
                Delivery = BeautifulSoup(data['del_message']).getText().replace('Delivered in','').replace('to your pincode','').replace('business','').strip()
            except:
                Delivery = ''
            
        except:
            COD = ''
            Delivery = ''

        try:
            EMI = soup.find(attrs = {'class':'prodEmiPopUpLink.mbs'}).getText()
            if EMI == '':
                EMI = soup.find(attrs = {'class':'pre-ext-emi-bg'}).getText()
        except:
            try:
                EMI = soup.find(attrs = {'class':'pre-ext-emi-bg'}).getText()
            except:
                EMI = ''
        try:
            breadcrums = soup.find(attrs = {'class':'breadcrumbWideDesign'}).findAll('li')[:-1]
            b = ''
            for bread in breadcrums:
                b = b + '|' + bread.getText().strip()
            Category_path = b[1:]
        except:
            Category_path = ''
        try:
            Description_Main = soup.find(attrs = {'class':'prd-attr-box.bb'}).getText().strip().replace('\n','')
        except:
            Description_Main = ''
        try:
            Short_Description = soup.find(attrs = {'class':'prd-attributes-item prd-attributes-shortDesc prd-attr-box'}).getText().strip().replace('\n','')
        except:
            Short_Description = ''
        try:
            soup.find(attrs = {'id':'careInstructions'}).click()
        except:
            pass
        try:
            Care_Instructions = soup.find(attrs = {'id':'careInstructions'}).getText()[20:].replace('\n','').strip()
        except:
            Care_Instructions = ''
        try:
            soup.find(attrs = {'id':'brandInformation'}).click()
        except:
            pass
        try:
            Brand_Information = soup.find(attrs = {'id':'brandInformation'}).getText()[18:].replace('\n','').strip()
        except:
            Brand_Information = ''
        try:
            soup.find(attrs = {'id':'#qa-Warranty'}).click()
        except:
            pass
        try:
            warranty = soup.find(attrs = {'id':'qa-Warranty'}).getText()
        except:
            warranty = ''

        if warranty != '' or Description_Main != ''  or Short_Description != ''  or Care_Instructions != '' \
           or Brand_Information!='':
            Description = str({'Description_Main':Description_Main, 'Short_Description':Short_Description,\
                       'Care_Instructions':Care_Instructions, 'Brand_Information':Brand_Information,\
                       'warranty':warranty})
        else:
            Description = ''
            
        Offers = ''
        try:
            s = soup.find(attrs = {'class':'prd-detailsWrapper-new'})
            Average_rating = float(int(s.find(attrs = {'class':'itm-ratStars itm-ratRating'})['style'].replace('width: ','').replace('%;',''))/20.0)
        except:
            Average_rating = ''
        try:
            soup.find(attrs = {'class':'fss reviewLhs'}).click()
        except:
            pass
        try:
            reviews = soup.findAll(attrs = {'class':'itm-ratRow mtm overflowH'})[:10]
            Reviews = ''
            for review in reviews:
                author = review.find(attrs = {'class':'itm-ratNickname'}).getText().replace('\n','').strip()
                description = review.find(attrs = {'class':'itm-ratComment fl w_80p bLeft'}).getText().replace('\n','').strip()
                Reviews += str({'author':author, 'description':description})
        except:
            Reviews = ''
        try:
            if soup.find(attrs = {'class':'i-addToCart cartTxt'}).getText().lower() == 'BUY NOW'.lower():
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
