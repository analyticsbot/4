from selenium import webdriver
from datetime import datetime

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
            PID = 'NA'
        URL_raw = url
        try:
            Title = driver.find_element_by_css_selector('.quickview-inner-rgt').find_element_by_tag_name('h1').text
        except:
            Title = 'NA'
        try:
            Brand = driver.find_element_by_css_selector('.orange-hd.txt_transform_UPC.font_size13').text
        except:
            Brand = 'NA'
        try:
            Seller = driver.find_element_by_css_selector('.seller_details').find_elements_by_tag_name('span')[1].text
        except:
            Seller = 'NA'
        try:
            IMG_medium = driver.find_element_by_css_selector('#Zoomer').find_element_by_tag_name('img').get_attribute('src')
        except:
            IMG_medium = 'NA'
        try:
            IMG_large = driver.find_element_by_css_selector('#Zoomer').get_attribute('href')
        except:
            IMG_large = 'NA'
        try:
            Price_mrp = driver.find_element_by_css_selector('#oldPriceAmntMainProd').text.strip()[1:].strip()
        except:
            Price_mrp = 'NA'
        try:
            Price_selling = driver.find_element_by_css_selector('#current_product_price').text.strip()
        except:
            Price_selling = 'NA'
        try:
            pincode = driver.find_element_by_css_selector('#pincode')
            pincode.send_keys('110001')
            pincode.submit()
            Price_shipping = ''
        except:
            Price_shipping = 'NA'
        try:
            Delivery = driver.find_element_by_css_selector('.product-page-border-bottom.stockDaysDetail').text
        except:
            Delivery = 'NA'
        try:
            COD = driver.find_element_by_css_selector('.stockDetailRow.stockCodDEtail').text.strip()
        except:
            COD = 'NA'
        try:
            EMI = ''
        except:
            EMI = 'NA'
        try:
            breadcrums = driver.find_element_by_css_selector('.breadcrums').find_elements_by_tag_name('li')
            b = ''
            for bread in breadcrums:
                b = b + '|' + bread.text.strip()
            Category_path = b.replace('|||','|')[1:]
        except:
            Category_path = 'NA'
        try:
            Description = 'Description: ' + driver.find_element_by_css_selector('.contents').text + '||Features: ' + driver.find_element_by_id('tab6').find_element_by_css_selector('.contents').text
        except:
            Description = 'NA'
        try:
            Offers = 'NA'
        except:
            Offers = 'NA'
        try:
            Average_rating = driver.find_element_by_css_selector('.product-page-review-rating').find_elements_by_tag_name('h2')[1].find_element_by_tag_name('span').text
        except:
            Average_rating = 'NA'
        try:
            Reviews = ''
            review_elem = driver.find_elements_by_css_selector('.reviews-count')[:10]
            for review in review_elem:
                try:
                    rating = review.find_element_by_css_selector('.starRating').find_elements_by_tag_name('meta')[1].get_attribute('content')
                except:
                    rating = 'NA'
                try:
                    author_date = review.find_element_by_css_selector('.starcol').text
                    author = author_date.split(',')[0].strip()
                    date = author_date.split(',')[1].strip()
                except:
                    author = 'NA'
                    date = 'NA'
                try:
                    headline = review.find_element_by_tag_name('h2').text
                except:
                    headline = 'NA'
                try:
                    description = review.find_element_by_tag_name('p').text
                except:
                    description = 'NA'
                Reviews = Reviews + str({'rating': str(rating), 'author':author, 'date':date, 'headline':headline,\
                                     'description':description}) + '||'
            Reviews = Reviews[:-2]
        except:
            Reviews = 'NA'
        try:
            Status = driver.find_element_by_css_selector('.head').text
        except:
            Status ="NA"
        Condition = 'NEW'
        TimeStamp = str(datetime.now())

        nrow = df.shape[0]
        df.loc[nrow+1] = [PID, URL_raw, Title, Brand,Seller, IMG_medium, IMG_large, Price_mrp, Price_selling, Price_shipping, Delivery,\
                          COD,EMI, Category_path,Description,Offers,Average_rating,Reviews,Status,Condition,TimeStamp]

        return df
