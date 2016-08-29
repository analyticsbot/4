from selenium import webdriver
from datetime import datetime


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
            
        try:
            PID = getData('Product Code')
        except:
            PID = 'NA'
        URL_raw = url
        try:
            Title = driver.find_element_by_css_selector('.img-description').find_element_by_tag_name('h1').text
        except:
            Title = 'NA'
        try:
            Brand = getData('Brand')
        except:
            Brand = 'NA'
        try:
            Seller = driver.find_element_by_css_selector('.profile-description').text.split('\n')[1]
        except:
            Seller = 'NA'
        try:
            IMG_medium = driver.find_element_by_css_selector('.img-dis').find_element_by_tag_name('img').get_attribute('src')
        except:
            IMG_medium = 'NA'
        try:
            IMG_large = driver.find_element_by_css_selector('.img-dis').find_element_by_tag_name('img').get_attribute('ng-src')
        except:
            IMG_large = 'NA'
        try:
            Price_mrp = driver.find_element_by_css_selector('.md-raised.fl.md-button.md-default-theme').find_element_by_tag_name('span').text.strip().replace('"','').split('|')[0].split('\n').replace('Buy for Rs ','').replace(',','')
        except:
            Price_mrp = 'NA'
        try:
            Price_selling = driver.find_element_by_css_selector('.md-raised.fl.md-button.md-default-theme').find_element_by_tag_name('span').text.strip().replace('"','').split('|')[0].split('\n').replace('Rs. ','').replace(',','')
        except:
            Price_selling = 'NA'
        try:
            zipcode = driver.find_element_by_css_selector('.ng-pristine.ng-valid.md-input.ng-valid-maxlength.ng-touched')
            zipcode.send_keys('110001')
            driver.find_element_by_css_selector('.apply').click()
        except:
            pass
        try:
            data = driver.find_element_by_css_selector('.detail-Shipp.dotted-border').find_elements_by_tag_name('li')
        except:
            data = ['NA']*4
        try:
            Price_shipping = data[3].text.replace('Shipping Charges: Rs ','')
        except:
            Price_shipping = 'NA'
        try:
            Delivery = data[0].text.replace('Shipping Charges: Rs ','')
        except:
            Delivery = 'NA'
        try:
            COD = data[1].text.replace('Cash on Delivery ','')
        except:
            COD = 'NA'
        try:
            EMI = driver.find_element_by_css_selector('.desc.dotted-border').find_element_by_tag_name('li').text
        except:
            EMI = 'NA'
        try:
            breadcrums = driver.find_element_by_css_selector('.breadcrum').find_elements_by_tag_name('a')
            b = ''
            for bread in breadcrums:
                b = b + '|' + bread.text.strip()
            Category_path = b[1:]
        except:
            Category_path = 'NA'
        try:
            Description = driver.find_element_by_css_selector('.ProductDescription').text
        except:
            Description = 'NA'
        try:
            Offers = driver.find_element_by_css_selector('.offer-cont').text
        except:
            Offers = 'NA'
        try:
            Average_rating = driver.find_element_by_css_selector('.rating-text').text
        except:
            Average_rating = 'NA'
        Reviews = 'NA'
        try:
            if driver.find_element_by_css_selector('.md-raised.fl.md-button.md-default-theme').find_element_by_tag_name('span').text.strip():
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
