from selenium import webdriver
from datetime import datetime
import time

class Snapdeal:
    def __init__(self):
        self.name = 'snapdeal'

    def Driver(self):
        self.driver = webdriver.Firefox()

    def closeDriver(self):
        self.driver.close()

    def scrapeData(self, url, df):
        self.driver.get(url)
        driver = self.driver
        driver = self.driver

        try:
            driver.find_element_by_css_selector('.sd-icon.sd-icon-delete-sign').click()
        except:
            pass
        attributes = driver.find_elements_by_css_selector('.linear_list')
        def getData(element):
            for attribute in attributes:
                if attribute.find_element_by_css_selector('.col1').text == element:
                    return attribute.find_element_by_css_selector('.col2').text
            
        PID = url.split('/')[-1]
        URL_raw = url
        try:
            Title = driver.find_element_by_css_selector('.pdp-e-i-head').text
        except:
            Title = ''
        try:
            Brand = driver.find_element_by_css_selector('.pdp-e-brand-logo-img').find_element_by_tag_name('img').get_attribute('alt')
        except:
            Brand = ''
        try:
            Seller = driver.find_element_by_css_selector('.pdp-e-seller-info-name.reset-margin').text
        except:
            Seller = ''
        try:
            IMG_medium = driver.find_element_by_css_selector('#bx-slider-left-image-panel').find_element_by_tag_name('img').get_attribute('src')
        except:
            IMG_medium = ''
        try:
            IMG_large = driver.find_element_by_css_selector('#bx-slider-left-image-panel').find_element_by_tag_name('img').get_attribute('bigsrc')
        except:
            IMG_large = ''
        try:
            Price_mrp = driver.find_element_by_css_selector('.pdpCutPrice').text.strip().replace('"','').replace(',','').replace('Rs.','').strip()
        except:
            Price_mrp = ''
        try:
            Price_selling = driver.find_element_by_css_selector('.payBlkBig').text.strip().replace(',','')
        except:
            Price_selling = Price_mrp

        if Price_mrp == '':
            Price_mrp = Price_selling

        try:
            pincode = driver.find_element_by_css_selector('#pincode-check')
            pincode.send_keys('110001')
            driver.find_element_by_id('pincode-check-bttn').click()
            time.sleep(2)
        except:
            pass
        try:
            Price_shipping = driver.find_element_by_css_selector('.freeDeliveryChargeCls.freeDeliveryCharge').\
                             text.replace('=-','')
            if 'Free Delivery' in Price_shipping:
                Price_shipping = 0
            elif 'Delivery Charges' in Price_shipping:
                Price_shipping = Price_shipping.replace(', Delivery Charges : +Rs','')
        except:
            Price_shipping = ''
        try:
            Delivery = driver.find_element_by_css_selector('.otoDRange').text.replace('Item will be delivered in','').replace('day(s) - Free Delivery','')
        except:
            Delivery = ''
        try:
            COD = driver.find_element_by_css_selector('#cod_status').text.strip()
        except:
            COD = ''
        try:
            driver.find_element_by_css_selector('.pdp-emi')
            EMI = 'Available'
        except:
            EMI = ''
        try:
            breadcrums = driver.find_element_by_css_selector('.bread-crumb').find_elements_by_tag_name('a')
            b = ''
            for bread in breadcrums:
                b = b + '|' + bread.text.strip()
            Category_path = b[1:]
        except:
            Category_path = ''
        try:
            Description = driver.find_element_by_css_selector('#productSpecs').text
        except:
            Description = ''

        try:
            Offers = driver.find_element_by_css_selector('.row.pdp-e-i-alloffers').text.split('\n')[0]
        except:
            Offers = ''
        try:
            Average_rating = driver.find_element_by_css_selector('.ig-star.star-y.sd-product-main-rating').get_attribute('md-data-rating')
        except:
            Average_rating = ''
        try:
            Reviews = driver.find_element_by_css_selector('.review_land.js-jl-omni.js-pdp-nav-sec').text
        except:
            Reviews = ''
        try:
            if driver.find_element_by_css_selector('.intialtext').text=='BUY NOW':
                Status = 'Available'
            else:
                Status = 'Sold Out'
        except:
            Status = 'Sold Out'

        Condition = 'NEW'
        TimeStamp = str(datetime.now())

        nrow = df.shape[0]
        df.loc[nrow+1] = [PID, URL_raw, Title, Brand,Seller, IMG_medium, IMG_large, Price_mrp, Price_selling, Price_shipping, Delivery,\
                          COD,EMI, Category_path,Description,Offers,Average_rating,Reviews,Status,Condition,TimeStamp]

        return df
