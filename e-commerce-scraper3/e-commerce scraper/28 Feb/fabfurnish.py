from selenium import webdriver
from datetime import datetime
import time
from selenium.webdriver.common.keys import Keys

class Fabfurnish:
    def __init__(self):
        self.name = 'fabfurnish'

    def Driver(self):
        self.driver = webdriver.Firefox()

    def closeDriver(self):
        self.driver.close()

    def scrapeData(self, url, df):
        self.driver.get(url)
        driver = self.driver
        time.sleep(2)
        try:
            city = driver.find_element_by_css_selector('#city')
            city.send_keys('Delh')
            city.send_keys(Keys.DOWN)
            city.send_keys(Keys.ENTER)
        except:
            pass

        try:
            PID = driver.find_element_by_css_selector('.prd_attr_desc.prd_attr_desc_wd').text
        except:
            PID = ''
        URL_raw = url
        try:
            Title = driver.find_element_by_css_selector('.prd-title-new').text
        except:
            Title = ''
        
        Seller = ''
        try:
            IMG_medium = driver.find_element_by_css_selector('.ad-image.example1').find_element_by_tag_name('img').get_attribute('src')
        except:
            IMG_medium = ''
        try:
            IMG_large = driver.find_element_by_css_selector('.ad-image.example1').find_element_by_tag_name('img').get_attribute('src')
        except:
            IMG_large = ''
        try:
            Price_mrp = driver.find_element_by_css_selector('#price_box').text.strip().replace(',','')
        except:
            Price_mrp = ''
        try:
            Price_selling = driver.find_element_by_css_selector('#special_price_box').text.strip().replace(',','')
        except:
            Price_selling = Price_mrp

        if Price_mrp == '':
            Price_mrp = Price_selling
            
        try:
            Price_shipping = driver.find_element_by_css_selector('#product-ship-charges').text
            if Price_shipping == None:
                Price_shipping = ''
        except:
            Price_shipping = ''
        try:
            pincode = driver.find_element_by_css_selector('#InputBoxpincode')
            pincode.send_keys('110001')
            driver.find_element_by_css_selector('.pincodBtnNewEstimate.mls').click()
        except:
            pass
        try:
            Delivery = driver.find_element_by_css_selector('.pincode_success').text.replace('Delivered in','').replace('business days to your pincode','').strip()
        except:
            Delivery = ''
        try:
            COD = driver.find_element_by_css_selector('.pre-ext-cod-bg.codavailText').text.strip()
        except:
            try:
                COD = driver.find_element_by_css_selector('.codavailText').text.strip()
            except:
                COD = ''
        try:
            EMI = driver.find_element_by_css_selector('.prodEmiPopUpLink.mbs').text
            if EMI == '':
                EMI = driver.find_element_by_css_selector('.pre-ext-emi-bg').text
        except:
            try:
                EMI = driver.find_element_by_css_selector('.pre-ext-emi-bg').text
            except:
                EMI = ''
        try:
            breadcrums = driver.find_element_by_css_selector('.breadcrumbWideDesign').find_elements_by_tag_name('li')[:-1]
            b = ''
            for bread in breadcrums:
                b = b + '|' + bread.text.strip()
            Category_path = b[1:]
        except:
            Category_path = ''
        try:
            Description_Main = driver.find_element_by_css_selector('.prd-attr-box.bb').text.strip().replace('\n','')
        except:
            Description_Main = ''
        try:
            Short_Description = driver.find_element_by_css_selector('.prd-attributes-item.prd-attributes-shortDesc.prd-attr-box').text.strip().replace('\n','')
        except:
            Short_Description = ''
        try:
            driver.find_element_by_css_selector('#careInstructions').click()
        except:
            pass
        try:
            Care_Instructions = driver.find_element_by_css_selector('#careInstructions').text[20:].replace('\n','').strip()
        except:
            Care_Instructions = ''
        try:
            driver.find_element_by_css_selector('#brandInformation').click()
        except:
            pass
        try:
            Brand_Information = driver.find_element_by_css_selector('#brandInformation').text[18:].replace('\n','').strip()
            Brand = Title.split()[0]
        except:
            Brand_Information = ''
        try:
            driver.find_element_by_css_selector('##qa-Warranty').click()
        except:
            pass
        try:
            warranty = driver.find_element_by_id('#qa-Warranty').text
        except:
            warranty = ''
        Description = str({'Description_Main':Description_Main, 'Short_Description':Short_Description,\
                       'Care_Instructions':Care_Instructions, 'Brand_Information':Brand_Information,\
                       'warranty':warranty})
        Offers = ''
        try:
            s = driver.find_element_by_css_selector('.prd-detailsWrapper-new')
            Average_rating = float(int(s.find_element_by_css_selector('.itm-ratStars.itm-ratRating').get_attribute('style').replace('width: ','').replace('%;',''))/20.0)
        except:
            Average_rating = ''
        try:
            driver.find_element_by_css_selector('.fss.reviewLhs').click()
        except:
            pass
        try:
            reviews = driver.find_elements_by_css_selector('.itm-ratRow.mtm.overflowH')[:10]
            Reviews = ''
            for review in reviews:
                author = review.find_element_by_css_selector('.itm-ratNickname').text.replace('\n','').strip()
                description = review.find_element_by_css_selector('.itm-ratComment.fl.w_80p.bLeft').text.replace('\n','').strip()
                Reviews += str({'author':author, 'description':description})
        except:
            Reviews = ''
        try:
            if driver.find_element_by_css_selector('.i-addToCart.cartTxt').text == 'BUY NOW':
                Status = 'IN STOCK'
            else:
                Status = 'OUT OF STOCK'
        except:
            Status = 'OUT OF STOCK'
        Condition = 'NEW'
        TimeStamp = str(datetime.now())

        nrow = df.shape[0]
        df.loc[nrow+1] = [PID, URL_raw, Title, Brand,Seller, IMG_medium, IMG_large, Price_mrp, Price_selling, Price_shipping, Delivery,\
                          COD,EMI, Category_path,Description,Offers,Average_rating,Reviews,Status,Condition,TimeStamp]

        return df
