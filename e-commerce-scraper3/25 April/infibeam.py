import mechanize
from datetime import datetime
from bs4 import BeautifulSoup

class Infobeam:
    def __init__(self):
        self.name = 'infobeam'

    def soup(self):
        self.driver = mechanize.Browser()

    def closesoup(self):
        self.driver.close()

    def scrapeData(self, url, df):        
        driver = self.driver
        driver.open(url)
        html = driver.response().read()
        soup = BeautifulSoup(html)
        
        PID = url.split('/')[-1].split('-')[2]
        URL_raw = url
        try:
            Title = soup.find(attrs = {'id':'title'}).getText().replace('"','').replace('\n','')
        except:
            Title = ''
        try:
            Brand = Title.split()[0]
        except:
            Brand = ''
        try:
            Seller = soup.find(attrs = {'class':'seller-detail name'}).getText()
        except:
            Seller = ''
        try:
            IMG_medium = soup.find(attrs = {'class':'hidden'})['src']
        except:
            IMG_medium = ''
        try:
            IMG_large = soup.find(attrs = {'class':'hidden'})['src']
        except:
            IMG_large = ''
        try:
            Price_mrp = soup.find(attrs = {'class':'price.linethrough'}).getText().strip().replace(',','')
        except:
            Price_mrp = ''
        try:
            Price_selling = soup.find(attrs = {'id':'price-after-discount'}).getText().strip()[1:].replace(',','').strip()
        except:
            Price_selling = Price_mrp

        if Price_mrp =='':
            Price_mrp = Price_selling
        try:
            selListingId = soup.find('input', attrs = {'class':'selListingId'})['value']
            uu = 'http://www.infibeam.com/rest/api/v1/variants/' + selListingId +'/isServiceable.json?zip=110001&variant_id=' + selListingId
            resp = requests.get(uu)
            COD = dict(eval(resp.content.replace('true', 'True').replace('false', 'False')))['result']['cod']
            if COD == True:
                COD = 'Available'
            else:
                COD = 'Not Available'
        except:
            pass
        try:
            Price_shipping = soup.find(attrs = {'class':'shipping-charge'}).getText()[1:].strip()
        except:
            try:
                if 'FREE Shipping' in str(soup):
                    Price_shipping = 0
                else:
                    Price_shipping = ''
            except:
                Price_shipping = ''
        try:
            Delivery = soup.find(attrs = {'class':'shipping_duration'}).getText().replace('Ships in','').strip()
        except:
            Delivery = ''

        try:
            soup.find(attrs = {'class':'emi-text'}).getText().strip()
            EMI = 'Available'
        except:
            EMI = 'Not Available'
        try:
            breadcrums = soup.find(attrs = {'class':'breadcrumb-sdp.no-padding-xs'}).findAll('a')
            b = ''
            for bread in breadcrums:
                b = b + '|' + bread.getText().strip()
            #Category_path = b + '|' + soup.find(attrs = {'class':'breadcrumb-sdp.no-padding-xs').find(attrs = {'class':'active').getText().replace('"','')
            Category_path = Category_path[1:]
        except:
            Category_path =''
        try:
            Description = soup.find(attrs = {'class':'catalog-desc'}).getText().replace('\n','').strip()
        except:
            Description = ''
        try:
            Offers = soup.find(attrs = {'class':'offer.coupon-code'}).getText().replace('\n','').strip()
        except:
            Offers = ''
        try:
            Average_rating = soup.find(attrs = {'class':'rating-star'}).find('img')['alt'].replace('Rating of','').replace('out of 5','').strip()
        except:
            Average_rating = ''
        try:
            Reviews = ''
            reviews = soup.findAll(attrs = {'class':'review'})
            for review in reviews:
                author = review.find('b').getText().strip()
                date = review.find(attrs = {'class':'easy-date'}).getText().strip()
                description = review.find(attrs = {'class':'review-text'}).getText().strip()
                Reviews += str({'author':author, 'date':date, 'description':description }) + '; '
            Reviews = Reviews[:-1]
        except:
            Reviews = ''
        try:
            if soup.find(attrs = {'class':'buyimg.buy-image.btn-image-express'})['value'] == 'BUY NOW':
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
