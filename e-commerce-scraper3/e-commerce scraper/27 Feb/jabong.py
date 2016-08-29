from selenium import webdriver
from datetime import datetime

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
        driver = self.driver


        product_details = driver.find_element_by_css_selector('.prod-main-wrapper').find_elements_by_tag_name('li')
        def getElement(element):
            for product_detail in product_details:
                name = product_detail.find_element_by_tag_name('label').text.strip()
                if name == element:
                    return product_detail.find_element_by_tag_name('span').text.strip()
            
        try:
            PID = getElement('SKU')
        except:
            PID = 'NA'
        URL_raw = url
        try:
            Title = driver.find_element_by_css_selector('.product-title').text
        except:
            Title = 'NA'
        try:
            Brand = driver.find_element_by_css_selector('.brand').text
        except:
            Brand = 'NA'
        Seller = 'Jabong'
        try:
            IMG_medium = driver.find_element_by_css_selector('.slide.slick-slide').find_element_by_tag_name('img').get_attribute('src')
        except:
            IMG_medium = 'NA'
        try:
            IMG_large = driver.find_element_by_css_selector('.slide.slick-slide').find_element_by_tag_name('img').get_attribute('data-src-1600')
        except:
            IMG_large = 'NA'
        try:
            Price_mrp = driver.find_element_by_css_selector('.standard-price').text.strip().replace('"','')
        except:
            Price_mrp = 'NA'
        try:
            Price_selling = driver.find_element_by_css_selector('.actual-price').text.strip().replace('"','')
        except:
            Price_selling = 'NA'
        try:
            driver.find_element_by_id('pdp-zip-link').click()
            d = driver.find_element_by_id('pdp-tat')
            a = d.find_element_by_tag_name('input')
            a.send_keys('110001')
        except:
            pass
        try:
            driver.find_element_by_css_selector('.input-group-addon.btn-primary.change-pincode').click()
        except:
            pass
        Price_shipping = 'FREE'
        try:
            Delivery = driver.find_element_by_id('pdp-tat-tool-tip').text.split('|')[0]
        except:
            Delivery = 'NA'
        try:
            COD = driver.find_element_by_id('pdp-tat-tool-tip').text.split('|')[1]
        except:
            COD = 'NA'
        EMI = ''
        try:
            breadcrums = driver.find_element_by_css_selector('.breadcrumb').find_elements_by_tag_name('a')
            b = ''
            for bread in breadcrums:
                b = b + '|' + bread.text.strip()
            Category_path = b[1:]
        except:
            Category_path = 'NA'
        try:
            Description = driver.find_element_by_css_selector('.prod-info').text
        except:
            Description = 'NA'
        Offers = 'NA'
        try:
            Average_rating = driver.find_element_by_css_selector('.current-rating').text
        except:
            Average_rating = 'NA'
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
            Reviews = 'NA'
        try:
            driver.find_element_by_css_selector('.sold-product')
            Status = 'Sold Out'
        except:
            Status = 'Available'
        Condition = 'NEW'
        TimeStamp = str(datetime.now())

        nrow = df.shape[0]
        df.loc[nrow+1] = [PID, URL_raw, Title, Brand,Seller, IMG_medium, IMG_large, Price_mrp, Price_selling, Price_shipping, Delivery,\
                          COD,EMI, Category_path,Description,Offers,Average_rating,Reviews,Status,Condition,TimeStamp]

        return df
