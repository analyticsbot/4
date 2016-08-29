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
            Title = 'NA'
        Brand = Title.split()[0]
        try:
            Seller = driver.find_element_by_css_selector('.seller-detail.name').text
        except:
            Seller = 'NA'
        try:
            IMG_medium = driver.find_element_by_css_selector('.img-responsive.inview').get_attribute('src')
        except:
            IMG_medium = 'NA'
        try:
            IMG_large = driver.find_element_by_css_selector('.hidden').get_attribute('src')
        except:
            IMG_large = 'NA'
        try:
            Price_mrp = driver.find_element_by_css_selector('.price.linethrough').text.strip().replace(',','')
        except:
            Price_mrp = 'NA'
        try:
            Price_selling = driver.find_element_by_css_selector('#price-after-discount').text.strip()[1:].replace(',','').strip()
        except:
            Price_selling = 'NA'
        try:
            zipcode = driver.find_element_by_id('zipCode')
            zipcode.send_keys('110001')
            driver.find_element_by_id('zipCheckSubmit').click()
        except:
            pass
        try:
            Price_shipping = driver.find_element_by_css_selector('.shipping-charge').text[1:].strip()
        except:
            Price_shipping = 'NA'
        try:
            Delivery = driver.find_element_by_css_selector('.shipping_duration').text
        except:
            Delivery = 'NA'
        try:
            COD = driver.find_element_by_css_selector('.stockDetailRow.stockCodDEtail').text.strip()
        except:
            COD  = driver.find_element_by_css_selector('.codSpan').text.strip()
        try:
            EMI = driver.find_element_by_css_selector('.emi-text').text
        except:
            EMI = 'NA'
        try:
            breadcrums = driver.find_element_by_css_selector('.breadcrumb-sdp.no-padding-xs').find_elements_by_tag_name('a')
            b = ''
            for bread in breadcrums:
                b = b + '|' + bread.text.strip()
            Category_path = b + '|' + driver.find_element_by_css_selector('.breadcrumb-sdp.no-padding-xs').find_element_by_css_selector('.active').text.replace('"','')
        except:
            Category_path ='NA'
        try:
            Description = driver.find_element_by_css_selector('.catalog-desc').text
        except:
            Description = 'NA'
        try:
            Offers = driver.find_element_by_css_selector('.offer.coupon-code').text
        except:
            Offers = 'NA'
        try:
            Average_rating = driver.find_element_by_css_selector('.rating-star').find_element_by_tag_name('img').get_attribute('alt')
        except:
            Average_rating = 'NA'
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
            Reviews = 'NA'
        try:
            if driver.find_element_by_css_selector('.buyimg.buy-image.btn-image-express').get_attribute('value') == 'BUY NOW':
                Status = 'Available'
            else:
                Status = 'Not Available'
        except:
            Status = 'Not Available'
        Condition = 'NEW'
        TimeStamp = str(datetime.now())

        nrow = df.shape[0]
        df.loc[nrow+1] = [PID, URL_raw, Title, Brand,Seller, IMG_medium, IMG_large, Price_mrp, Price_selling, Price_shipping, Delivery,\
                          COD,EMI, Category_path,Description,Offers,Average_rating,Reviews,Status,Condition,TimeStamp]

        return df
