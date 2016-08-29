from selenium import webdriver
from datetime import datetime
import time, re

class Pepperfry:
    def __init__(self):
        self.name = 'pepperfry'

    def Driver(self):
        self.driver = webdriver.Firefox()
        driver = self.driver

    def closeDriver(self):
        self.driver.close()

    def scrapeData(self, url, df):
        self.driver.get(url)
        driver = self.driver
        driver = self.driver

        try:
            attributes = driver.find_elements_by_css_selector('.vip-dtl-desc')
        except:
            attributes = ''
            
        def getData(element):
            for attribute in attributes:
                if attribute.find_element_by_tag_name('b').text.strip() == element:
                    return attribute.find_element_by_tag_name('span').text
            
        try:
            PID = getData('Sku:')
        except:
            PID = ''
        URL_raw = url
        try:
            Title = driver.find_element_by_css_selector('.vip-product-title').text
        except:
            Title = ''
        try:
            Brand = getData('Brand:')
        except:
            Brand = ''
        try:
            Seller = driver.find_element_by_css_selector('.more-from-brand').text.replace('More From ','')
        except:
            Seller = ''
        try:
            IMG_medium = driver.find_element_by_css_selector('#vipImage').find_element_by_tag_name('img').get_attribute('src')
        except:
            IMG_medium = ''
        try:
            IMG_large = driver.find_element_by_id('bigImageContainer').get_attribute('src')
        except:
            IMG_large = ''
        try:
            Price_mrp = driver.find_element_by_css_selector('.vip-prices').find_elements_by_tag_name('li')[0].text.strip().replace('"','').replace('Retail Price: Rs.','').replace(',','')
            Price_mrp = re.compile(r'(\d+)').search(Price_mrp).group(0)
        except:
            Price_mrp = ''
        try:
            Price_selling = driver.find_element_by_css_selector('.vip-prices').find_elements_by_tag_name('li')[1].text.strip().replace(',','').replace('Offer Price: Rs.','').replace(',','')
        except:
            Price_selling = Price_mrp

        if Price_mrp == '':
            Price_mrp = Price_selling

        try:
            pincode = driver.find_element_by_css_selector('#pincode')
            pincode.send_keys('110001')
            driver.find_element_by_css_selector('#vipPincodeSub').click()
            time.sleep(3)
        except:
            pass
        try:
            Price_shipping = driver.find_element_by_css_selector('.tdcolor1').text
        except:
            Price_shipping = ''
        try:
            Delivery = driver.find_element_by_css_selector('#delivery_status').text
            if Delivery == '':
                try:
                    Delivery = driver.find_element_by_css_selector('.vip-pin-success-txt').text
                except:
                    Delivery = ''
        except:
            try:
                Delivery = driver.find_element_by_css_selector('.vip-pin-success-txt').text.split('\n')[0].replace('Order Today to get delivery between','').split('Assembly')[0]
            except:
                Delivery = ''
        try:
            driver.find_element_by_css_selector('.vip-p-opt-img.vip-p-opt-fail')
            COD = 'Not Available'
        except:
            COD = 'Available'
        try:
            driver.find_element_by_id('emi_strip')
            EMI = 'Available'
        except:
            EMI = ''
        try:
            breadcrums = driver.find_element_by_css_selector('.breadcrumb.container').find_elements_by_tag_name('a')[:-1]
            b = ''
            for bread in breadcrums:
                b = b + '|' + bread.text.strip()
            Category_path = b[1:]
        except:
            Category_path = ''
        try:
            Description = driver.find_element_by_css_selector('.vip-dtl-para').text
        except:
            Description = ''

        try:
            Offers = driver.find_element_by_css_selector('.vip-offer-text').text
        except:
            try:
                Offers = driver.find_element_by_css_selector('.vip-cpn-box').text
            except:
                Offers = ''
        try:
            Average_rating = driver.find_element_by_css_selector('.rating-text').text
        except:
            Average_rating = ''
        Reviews = ''
        try:
            driver.find_element_by_css_selector('.vip-buy-now-each.third.inactive')
            Status = 'OUT OF STOCK'
                          
        except:
            Status = 'IN STOCK'  

        Condition = 'NEW'
        TimeStamp = str(datetime.now())

        nrow = df.shape[0]
        df.loc[nrow+1] = [PID, URL_raw, Title, Brand,Seller, IMG_medium, IMG_large, Price_mrp, Price_selling, Price_shipping, Delivery,\
                          COD,EMI, Category_path,Description,Offers,Average_rating,Reviews,Status,Condition,TimeStamp]

        return df
