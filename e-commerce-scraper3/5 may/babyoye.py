from selenium import webdriver
from datetime import datetime
import time

class Babyoye:
    def __init__(self):
        self.name = 'babyoye'

    def Driver(self):
        self.driver = webdriver.Firefox()

    def closeDriver(self):
        self.driver.close()

    def scrapeData(self, url, df):
        self.driver.get(url)
        driver = self.driver

        try:
            PID = url.split('/')[-1]
        except:
            PID = ''
        URL_raw = url
        try:
            Title = driver.find_element_by_css_selector('.quickview-inner-rgt').find_element_by_tag_name('h1').text
        except:
            Title = ''
        try:
            Brand = driver.find_element_by_css_selector('.orange-hd.txt_transform_UPC.font_size13').text
        except:
            Brand = ''
        try:
            Seller = driver.find_element_by_css_selector('.seller_details').find_elements_by_tag_name('span')[1].text
        except:
            Seller = ''
        try:
            IMG_medium = driver.find_element_by_css_selector('#Zoomer').find_element_by_tag_name('img').get_attribute('src')
        except:
            IMG_medium = ''
        try:
            IMG_large = driver.find_element_by_css_selector('#Zoomer').get_attribute('href')
        except:
            IMG_large = ''
        try:
            Price_mrp = driver.find_element_by_css_selector('#oldPriceAmntMainProd').text.strip()[1:].strip().replace(",",'')
        except:
            Price_mrp = ''
        try:
            Price_selling = driver.find_element_by_css_selector('#current_product_price').text.strip().replace(",",'')
        except:
            if Price_mrp !='':
                Price_selling = Price_mrp
            else:
                Price_selling = ''

        if Price_mrp == '' and Price_selling != '':
            Price_mrp = Price_selling

        try:
            color = driver.find_element_by_css_selector('.selection_color').find_elements_by_tag_name('img')
            color[0].click()
        except:
            pass
        try:
            pincode = driver.find_element_by_css_selector('#pincode')
            pincode.send_keys('110001')
            driver.find_element_by_id('deliveryAndCodDetailCheck').click()
            time.sleep(2)
        except:
            pass
        try:
            if int(float(Price_mrp))>499:
                Price_shipping = 0
            else:
                Price_shipping = 50
        except:
            Price_shipping = ''
        try:
            Delivery = driver.find_element_by_css_selector('.product-page-border-bottom.stockDaysDetail').text.replace('Delivers in','').strip()
        except:
            Delivery = ''
        try:
            COD = driver.find_element_by_css_selector('.stockDetailRow.stockCodDEtail').text.replace('Cash On Delivery','').strip()
        except:
            COD = ''
        try:
            EMI = ''
        except:
            EMI = ''
        try:
            breadcrums = driver.find_element_by_css_selector('.breadcrums').find_elements_by_tag_name('li')
            b = ''
            for bread in breadcrums:
                b = b + '|' + bread.text.strip()
            Category_path = b.replace('|||','|')[1:]
        except:
            Category_path = ''
        try:
            Description = str({'Description': driver.find_element_by_css_selector('.contents').text, \
                          'Features':driver.find_element_by_id('tab6').find_element_by_css_selector('.contents').text})
        except:
            Description = ''
        try:
            Offers = ''
        except:
            Offers = ''
        try:
            Average_rating = driver.find_element_by_css_selector('.product-page-review-rating').find_elements_by_tag_name('h2')[1].find_element_by_tag_name('span').text
        except:
            Average_rating = ''
        try:
            Reviews = ''
            review_elem = driver.find_elements_by_css_selector('.reviews-count')[:10]
            for review in review_elem:
                try:
                    rating = review.find_element_by_css_selector('.starRating').find_elements_by_tag_name('meta')[1].get_attribute('content')
                except:
                    rating = ''
                try:
                    author_date = review.find_element_by_css_selector('.starcol').text
                    author = author_date.split(',')[0].strip()
                    date = author_date.split(',')[1].strip()
                except:
                    author = ''
                    date = ''
                try:
                    headline = review.find_element_by_tag_name('h2').text
                except:
                    headline = ''
                try:
                    description = review.find_element_by_tag_name('p').text
                except:
                    description = ''
                Reviews = Reviews + str({'rating': str(rating), 'author':author, 'date':date, 'headline':headline,\
                                     'description':description}) + '||'
            Reviews = Reviews[:-2]
        except:
            Reviews = ''
        try:
            driver.find_element_by_css_selector('.temporarily_outof_stock.algncenter.fnt14s')
            Status = 'OUT OF STOCK'    
        except:
            try:
                driver.find_element_by_css_selector('.stockDetail.in-stock-details')
                Status = 'IN STOCK'   
            except:
                Status = ''
        Condition = 'NEW'
        TimeStamp = str(datetime.now())

        nrow = df.shape[0]
        df.loc[nrow+1] = [PID, URL_raw, Title, Brand,Seller, IMG_medium, IMG_large, Price_mrp, Price_selling, Price_shipping, Delivery,\
                          COD,EMI, Category_path,Description,Offers,Average_rating,Reviews,Status,Condition,TimeStamp]

        return df
