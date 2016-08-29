from selenium import webdriver
from datetime import datetime
import time

class Paytm:
    def __init__(self):
        self.name = 'paytm'

    def Driver(self):
        self.driver = webdriver.Firefox()

    def closeDriver(self):
        self.driver.close()

    def scrapeData(self, url, df):
        self.driver.get(url)
        driver = self.driver
        driver = self.driver


        attributes = driver.find_elements_by_css_selector('.attributes')
        def getData(element):
            for attribute in attributes:
                if attribute.find_element_by_css_selector('.col1').text == element:
                    return attribute.find_element_by_css_selector('.col2').text

        def getFields(data, element):
            for d in data:
                if element in d.text:
                    return 'Available'
                elif 
            
        try:
            PID = getData('Product Code')
        except:
            PID = ''
        URL_raw = url
        try:
            Title = driver.find_element_by_css_selector('.img-description').find_element_by_tag_name('h1').text
        except:
            Title = ''
        try:
            Brand = getData('Brand')
        except:
            Brand = ''
        try:
            Seller = driver.find_element_by_css_selector('.profile-description').text.split('\n')[1]
        except:
            Seller = ''
        try:
            IMG_medium = driver.find_element_by_css_selector('.img-dis').find_element_by_tag_name('img').get_attribute('src')
        except:
            IMG_medium = ''
        try:
            IMG_large = driver.find_element_by_css_selector('.img-dis').find_element_by_tag_name('img').get_attribute('ng-src')
        except:
            IMG_large = ''
        try:
            Price_mrp = driver.find_element_by_css_selector('.md-raised.fl.md-button.md-default-theme').find_element_by_tag_name('span')\
                        .text.strip().replace('"','').split('|')[0].replace('Buy for Rs ','').replace(',','').split('\n')[1].replace('Rs.','')
        except:
            Price_mrp = ''
        try:
            Price_selling = driver.find_element_by_css_selector('.md-raised.fl.md-button.md-default-theme').find_element_by_tag_name('span')\
                            .text.strip().replace('"','').split('|')[0].replace('Rs. ','').replace(',','').replace('Buy for Rs ','').split('\n')[0]
        except:
            Price_selling = Price_mrp

        if Price_mrp == '':
           Price_mrp =  Price_selling
        try:
            zipcode = driver.find_element_by_css_selector('.ng-pristine.ng-valid.md-input.ng-valid-maxlength.ng-touched')
            zipcode.send_keys('110001')
            driver.find_element_by_css_selector('.apply').click()
        except:
            pass
        time.sleep(1)
        try:
            data = driver.find_element_by_css_selector('.detail-Shipp.dotted-border').find_elements_by_tag_name('li')
        except:
            data = ''
        try:
            for d in data:
                if 'Shipping Charges' in d.text:
                    Price_shipping = d.text.replace('Shipping Charges: Rs','')
                elif 'Shipping : Free' in d.text:
                    Price_shipping = 0
        except:
            Price_shipping = ''
        try:
            for d in data:
                if 'Delivery available' in d.text:
                    Delivery = 'Available'
                elif 'Delivery not available' in d.text:
                    Delivery = 'Not Available'
        except:
            Delivery = 'Not Available'
        try:
            for d in data:
                if 'Cash on Delivery available' in d.text:
                    COD = 'Available'
                elif 'Cash on Delivery not available' in d.text:
                    COD = 'Not Available'
        except:
            COD = 'Not Available'
        try:
            EMI = ''
        except:
            EMI = ''
        try:
            breadcrums = driver.find_element_by_css_selector('.breadcrum').find_elements_by_tag_name('a')
            b = ''
            for bread in breadcrums:
                b = b + '|' + bread.text.strip()
            Category_path = b[1:]
        except:
            Category_path = ''
        try:
            Description = driver.find_element_by_css_selector('.ProductDescription').text
        except:
            Description = ''
        try:
            Offers = driver.find_element_by_css_selector('.offer-cont').text
        except:
            Offers = ''
        try:
            Average_rating = driver.find_element_by_css_selector('.rating-text').text.replace('/5','').replace('ratings','')
        except:
            Average_rating = ''
        Reviews = ''
        try:
            if driver.find_element_by_css_selector('.md-raised.fl.md-button.md-default-theme').find_element_by_tag_name('span').text.strip():
                Status = 'IN STOCK'
            else:
                Status = 'OUT OF STOCK'
            if 'Out of stock' in driver.page_source:
                Status = 'OUT OF STOCK'
            else:
                Status = 'IN STOCK'
        except:
            if 'Out of stock' in driver.page_source:
                Status = 'OUT OF STOCK'
            else:
                Status = 'IN STOCK'

        Condition = 'NEW'
        TimeStamp = str(datetime.now())

        nrow = df.shape[0]
        df.loc[nrow+1] = [PID, URL_raw, Title, Brand,Seller, IMG_medium, IMG_large, Price_mrp, Price_selling, Price_shipping, Delivery,\
                          COD,EMI, Category_path,Description,Offers,Average_rating,Reviews,Status,Condition,TimeStamp]

        return df
