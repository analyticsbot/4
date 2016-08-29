from selenium import webdriver
from datetime import datetime

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

        attributes = driver.find_element_by_css_selector('.linear_list').find_elements_by_tag_name('li')
        def getData(element):
            for attribute in attributes:
                if attribute.find_element_by_tag_name('strong').text == element:
                    return attribute.find_element_by_tag_name('span').text
            
        try:
            PID = getData('Sku:')
        except:
            PID = 'NA'
        URL_raw = url
        try:
            Title = driver.find_element_by_css_selector('.vip-product-title').text
        except:
            Title = 'NA'
        Brand = Title.split()[0]
        try:
            Seller = driver.find_element_by_css_selector('.more-from-brand').text.replace('More From ','')
        except:
            Seller = 'NA'
        try:
            IMG_medium = driver.find_element_by_css_selector('#vipImage').find_element_by_tag_name('img').get_attribute('src')
        except:
            IMG_medium = 'NA'
        try:
            IMG_large = driver.find_element_by_id('bigImageContainer').get_attribute('src')
        except:
            IMG_large = 'NA'
        try:
            Price_mrp = driver.find_element_by_css_selector('.vip-prices').find_elements_by_tag_name('li')[0].text.strip().replace('"','').replace('Retail Price: Rs.','').replace(',','')
        except:
            Price_mrp = 'NA'
        try:
            Price_selling = driver.find_element_by_css_selector('.vip-prices').find_elements_by_tag_name('li')[1].text.strip().replace(',','').replace('Offer Price: Rs.','').replace(',','')
        except:
            Price_selling = 'NA'

        try:
            pincode = driver.find_element_by_css_selector('#pincode')
            pincode.send_keys('110001')
            driver.find_element_by_css_selector('.vip-pinenter').click()
            time.sleep(3)
        except:
            pass
        try:
            Price_shipping = driver.find_element_by_css_selector('.tdcolor1').text
        except:
            Price_shipping = 'NA'
        try:
            Delivery = driver.find_element_by_css_selector('#delivery_status').text
        except:
            Delivery = 'NA'
        try:
            COD = driver.find_element_by_css_selector('#cod_status').text.strip()
        except:
            COD = 'NA'
        EMI = ''
        try:
            breadcrums = driver.find_element_by_css_selector('.breadcrumb.container').find_elements_by_tag_name('a')
            b = ''
            for bread in breadcrums:
                b = b + '|' + bread.text.strip()
            Category_path = b[1:]
        except:
            Category_path = 'NA'
        try:
            Description = driver.find_element_by_css_selector('.other_details_body').text + driver.find_element_by_css_selector('.other_details_panel.gb-scroll').text
        except:
            Description = 'NA'

        try:
            Offers = driver.find_element_by_css_selector('.vip-offer-text').text
        except:
            Offers = 'NA'
        try:
            Average_rating = driver.find_element_by_css_selector('.rating-text').text
        except:
            Average_rating = 'NA'
        Reviews = 'NA'
        Status = driver.find_element_by_css_selector('.quantity-left').text

        Condition = 'NEW'
        TimeStamp = str(datetime.now())

        nrow = df.shape[0]
        df.loc[nrow+1] = [PID, URL_raw, Title, Brand,Seller, IMG_medium, IMG_large, Price_mrp, Price_selling, Price_shipping, Delivery,\
                          COD,EMI, Category_path,Description,Offers,Average_rating,Reviews,Status,Condition,TimeStamp]

        return df
