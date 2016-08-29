from datetime import datetime
import time, mechanize, requests, re, json
from bs4 import BeautifulSoup

class Babyoye:
    def __init__(self):
        self.name = 'babyoye'

    def Driver(self):
        self.driver = mechanize.Browser()

    def closeDriver(self):
        self.driver.close()

    def scrapeData(self, url, df):
        self.driver.open(url)
        driver = self.driver
        html = driver.response().read()
        soup = BeautifulSoup(html)

        try:
            PID = url.split('/')[-1]
        except:
            PID = ''
        URL_raw = url
        try:
            Title = soup.find(attrs = {'class':'quickview-inner-rgt'}).find('h1').getText().replace('\n','')
        except:
            Title = ''
        try:
            Brand = soup.find(attrs = {'class':'orange-hd txt_transform_UPC font_size13'}).getText()
        except:
            Brand = ''
        try:
            Seller = soup.find(attrs = {'class':'seller_details'}).findAll('span')[1].getText()
        except:
            Seller = ''
        try:
            IMG_medium = soup.find(attrs = {'id':'Zoomer'}).find('img')['src']
        except:
            IMG_medium = ''
        try:
            IMG_large = soup.find(attrs = {'id':'Zoomer'})['href']
        except:
            IMG_large = ''
        try:
            Price_mrp = soup.find(attrs = {'id':'oldPriceAmntMainProd'}).getText().strip()[1:].strip().replace(",",'')
        except:
            Price_mrp = ''
        try:
            Price_selling = soup.find(attrs = {'id':'current_product_price'}).getText().strip().replace(",",'')
        except:
            if Price_mrp !='':
                Price_selling = Price_mrp
            else:
                Price_selling = ''

        if Price_mrp == '' and Price_selling != '':
            Price_mrp = Price_selling

        try:
            if int(float(Price_mrp))>499:
                Price_shipping = 0
            else:
                Price_shipping = 50
        except:
            Price_shipping = ''

        try:
            EMI = ''
        except:
            EMI = ''
        try:
            breadcrums = soup.find(attrs = {'class':'breadcrums'}).findAll('li')
            b = ''
            for bread in breadcrums:
                b = b + '|' + bread.getText().strip()
            Category_path = b.replace('|||','|')[1:].replace('&AMP;','&')
        except:
            Category_path = ''
        try:
            Description = str({'Description': ' '.join(soup.find(attrs = {'class':'contents'}).getText().split()), \
                          'Features': ' '.join(soup.find(attrs = {'id':'tab6'}).find(attrs = {'class':'contents'}).getText().strip().replace('\\r\\n', ' ').replace('\\n',' ').split())})
        except:
            Description = ''
        try:
            Offers = ''
        except:
            Offers = ''
        try:
            Average_rating = soup.find(attrs = {'class':'product-page-review-rating'}).findAll('h2')[1].find('span').getText()
        except:
            Average_rating = ''
        try:
            Reviews = ''
            review_elem = soup.findAll(attrs = {'class':'reviews-count'})[:10]
            for review in review_elem:
                try:
                    rating = review.find(attrs = {'class':'starRating'}).findAll('meta')[1]['content']
                except:
                    rating = ''
                try:
                    author_date = review.find(attrs = {'class':'starcol'}).getText()
                    author = author_date.split(',')[0].strip()
                    date = author_date.split(',')[1].strip()
                except:
                    author = ''
                    date = ''
                try:
                    headline = review.find('h2').getText()
                except:
                    headline = ''
                try:
                    description = review.find('p').getText()
                except:
                    description = ''
                Reviews = Reviews + str({'rating': str(rating), 'author':author, 'date':date, 'headline':headline,\
                                     'description':description}) + '||'
            Reviews = Reviews[:-2]
        except:
            Reviews = ''    

        try:
            my_regex = r"\"(" + Seller + ".*)\";if"
            facilityList = re.findall(my_regex, html)[0]
            data = {'pincode':'110001', 'productId':PID[2:], 'facilityList':facilityList}
            url_delivery = 'http://www.babyoye.com/control/deliveryAndCodDetail'
            res = requests.post(url_delivery, data = data)
            d = res.content
            Status = 'IN STOCK'  
        except:
            Status = 'OUT OF STOCK'
        try:
            Delivery = json.loads(d)['DEL_AND_COD_DETAIL']['deliveryTime']
        except:
            Delivery = ''
        try:
            COD = json.loads(d)['DEL_AND_COD_DETAIL']['codAvailable']
        except:
            COD = ''

        Condition = 'NEW'
        TimeStamp = str(datetime.now())

        nrow = df.shape[0]
        df.loc[nrow+1] = [PID, URL_raw, Title, Brand,Seller, IMG_medium, IMG_large, Price_mrp, Price_selling, Price_shipping, Delivery,\
                          COD,EMI, Category_path,Description,Offers,Average_rating,Reviews,Status,Condition,TimeStamp]

        return df
