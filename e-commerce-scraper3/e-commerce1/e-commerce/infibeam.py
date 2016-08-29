from selenium import webdriver
from datetime import datetime

class Infobeam:
    def __init__(self):
        self.name = 'infobeam'

    def Driver(self):
        self.driver = webdriver.Firefox()

    def closeDriver(self):
        self.driver.close()

    def scrapeData(self, url, df):
        self.driver.get(url)
        driver = self.driver
        
        PID = url.split('/')[-1].split('-')[2]
        URL_raw = url
        try:
            Title = driver.find_element_by_css_selector('#title').text.replace('"','')
        except:
            Title = ''
        try:
            Brand = Title.split()[0]
        except:
            Brand = ''
        try:
            Seller = driver.find_element_by_css_selector('.seller-detail.name').text
        except:
            Seller = ''
        try:
            IMG_medium = driver.find_element_by_css_selector('.img-responsive.inview').get_attribute('src')
        except:
            IMG_medium = ''
        try:
            IMG_large = driver.find_element_by_css_selector('.hidden').get_attribute('src')
        except:
            IMG_large = ''
        try:
            Price_mrp = driver.find_element_by_css_selector('.price.linethrough').text.strip().replace(',','')
        except:
            Price_mrp = ''
        try:
            Price_selling = driver.find_element_by_css_selector('#price-after-discount').text.strip()[1:].replace(',','').strip()
        except:
            Price_selling = Price_mrp

        if Price_mrp =='':
            Price_mrp = Price_selling
        try:
            zipcode = driver.find_element_by_id('zipCode')
            zipcode.send_keys('110001')
            driver.find_element_by_id('zipCheckSubmit').click()
        except:
            pass
        try:
            Price_shipping = driver.find_element_by_css_selector('.shipping-charge').text[1:].strip()
        except:
            try:
                if 'FREE Shipping' in driver.page_source:
                    Price_shipping = 0
            except:
                Price_shipping = ''
        try:
            Delivery = driver.find_element_by_css_selector('.shipping_duration').text.replace('Ships in','').strip()
        except:
            Delivery = ''
        try:
            COD = driver.find_element_by_css_selector('.stockDetailRow.stockCodDEtail').text.strip()
            if 'is available' in COD:
                COD = 'Available'
            else:
                COD = 'Not Available'
        except:
            try:
                COD  = driver.find_element_by_css_selector('.codSpan').text.strip()
                if 'is available' in COD:
                    COD = 'Available'
                else:
                    COD = 'Not Available'
            except:
                COD = ''
        try:
            driver.find_element_by_css_selector('.emi-text').text.strip()
            EMI = 'Available'
        except:
            EMI = 'Not Available'
        try:
            breadcrums = driver.find_element_by_css_selector('.breadcrumb-sdp.no-padding-xs').find_elements_by_tag_name('a')
            b = ''
            for bread in breadcrums:
                b = b + '|' + bread.text.strip()
            #Category_path = b + '|' + driver.find_element_by_css_selector('.breadcrumb-sdp.no-padding-xs').find_element_by_css_selector('.active').text.replace('"','')
            Category_path = Category_path[1:]
        except:
            Category_path =''
        try:
            Description = driver.find_element_by_css_selector('.catalog-desc').text.replace('\n','').strip()
        except:
            Description = ''
        try:
            Offers = driver.find_element_by_css_selector('.offer.coupon-code').text.replace('\n','').strip()
        except:
            Offers = ''
        try:
            Average_rating = driver.find_element_by_css_selector('.rating-star').find_element_by_tag_name('img').get_attribute('alt').replace('Rating of','').replace('out of 5','').strip()
        except:
            Average_rating = ''
        try:
            Reviews = ''
            reviews = driver.find_elements_by_css_selector('.review')
            for review in reviews:
                author = review.find_element_by_tag_name('b').text.strip()
                date = review.find_element_by_css_selector('.easy-date').text.strip()
                description = review.find_element_by_css_selector('.review-text').text.strip()
                Reviews += str({'author':author, 'date':date, 'description':description }) + '; '
            Reviews = Reviews[:-1]
        except:
            Reviews = ''
        try:
            if driver.find_element_by_css_selector('.buyimg.buy-image.btn-image-express').get_attribute('value') == 'BUY NOW':
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
