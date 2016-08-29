from selenium import webdriver
from datetime import datetime
import time, re

class Jabong:
    def __init__(self):
        self.name = 'jabong'

    def Driver(self):
        self.driver = webdriver.Firefox()

    def closeDriver(self):
        self.driver.close()

    def scrapeData(self, url, df):
        self.driver.get(url)
        driver = self.driver
        driver.maximize_window()
        
        try:
            product_details = driver.find_element_by_css_selector('.prod-main-wrapper').find_elements_by_tag_name('li')
            
            def getElement(element):
                for product_detail in product_details:
                    name = product_detail.find_element_by_tag_name('label').text.strip()
                    if name == element:
                        return product_detail.find_element_by_tag_name('span').text.strip()
        except:
            pass
        try:
            breadcrums = driver.find_element_by_css_selector('.breadcrumb').find_elements_by_tag_name('a')
            b = ''
            for bread in breadcrums:
                b = b + '|' + bread.text.strip()
            Category_path = b[1:]
            Category_path = re.sub(r'([|])\1+', '', Category_path).strip()
        except Exception,e:
            print str(e)
            Category_path = ''
        try:
            Description = driver.find_element_by_css_selector('.prod-info').text
        except:
            Description = ''
        try:
            Average_rating = driver.find_element_by_css_selector('.current-rating').text
        except:
            Average_rating = ''
        try:
            Reviews = ''
            reviews = driver.find_elements_by_css_selector('.review-wrapper.clearfix')
            for review in reviews:
                author = review.find_element_by_tag_name('b').text
                date = review.find_element_by_css_selector('.rating-timeline').text
                description = review.find_element_by_css_selector('.user-comment.col-md-9.col-sm-8.col-xs-12').text
                Reviews += str({'author':author, 'date':date, 'description':description}) + "; "
            Reviews = Reviews[:-1]
        except:
            Reviews = ''
        try:
            PID = getElement('SKU')
        except:
            PID = ''
        URL_raw = url
        try:
            Title = driver.find_element_by_css_selector('.product-title').text
        except:
            Title = ''
        try:
            Brand = driver.find_element_by_css_selector('.brand').text
        except:
            Brand = ''
        Seller = ''
        try:
            IMG_medium = driver.find_element_by_css_selector('.slide.slick-slide').find_element_by_tag_name('img').get_attribute('src')
        except:
            IMG_medium = ''
        try:
            driver.find_element_by_css_selector('.slide.slick-slide.slick-active').click()
            time.sleep(1)
            IMG_large = driver.find_element_by_css_selector('.slide.slick-slide.slick-active').find_element_by_tag_name('img').get_attribute('src')
        except:
            IMG_large = ''
        try:
            Price_mrp = driver.find_element_by_css_selector('.standard-price').text.strip().replace('"','')
        except:
            Price_mrp = ''
        try:
            Price_selling = driver.find_element_by_css_selector('.actual-price').text.strip().replace('"','')
        except:
            Price_selling = Price_mrp

        if Price_mrp == '':
            Price_mrp = Price_selling
            
        try:
            driver.find_element_by_id('pdp-zip-link').find_element_by_tag_name('a').click()
            d = driver.find_element_by_id('pdp-tat')
            a = d.find_element_by_tag_name('input')
            a.send_keys('110001')
            time.sleep(1)
        except:
            pass
        try:
            driver.find_element_by_css_selector('.input-group-addon.btn-primary.change-pincode').click()
        except:
            pass
        Price_shipping = ''
        try:
            Delivery = driver.find_element_by_id('pdp-tat-tool-tip').text.split('|')[0].strip().replace('DELIVERED BY','').strip().replace('DISPATCHED BY','')
        except:
            Delivery = ''
        try:
            COD = driver.find_element_by_id('pdp-tat-tool-tip').text.strip()
            if 'COD AVAILABLE' in COD:
                COD = 'Available'
            else:
                COD = 'Not Available'
        except:
            COD = ''
        EMI = ''
        
        
        Offers = ''
        
        try:
            driver.find_element_by_css_selector('.sold-product')
            Status = 'OUT OF STOCK'
        except:
            Status = 'IN STOCK'
        Condition = 'NEW'
        TimeStamp = str(datetime.now())

        nrow = df.shape[0]
        df.loc[nrow+1] = [PID, URL_raw, Title, Brand,Seller, IMG_medium, IMG_large, Price_mrp, Price_selling, Price_shipping, Delivery,\
                          COD,EMI, Category_path,Description,Offers,Average_rating,Reviews,Status,Condition,TimeStamp]

        return df
