from datetime import datetime
import time, re, requests
from bs4 import BeautifulSoup
import mechanize

class Pepperfry:
    def __init__(self):
        self.name = 'pepperfry'

    def Driver(self):
        self.driver = mechanize.Browser()

    def closeDriver(self):
        self.driver.close()

    def scrapeData(self, url, df):
        driver = self.driver
        driver.open(url)
        html = driver.response().read()
        soup = BeautifulSoup(html)

        try:
            attributes = soup.findAll(attrs = {'class':'vip-dtl-desc'})
        except:
            attributes = ''
            
        def getData(element):
            for attribute in attributes:
                if attribute.find('b').getText().strip() == element:
                    return attribute.find('span').getText()
            
        try:
            PID = getData('Sku:')
        except:
            PID = ''
        URL_raw = url
        try:
            Title = soup.find(attrs = {'class':'vip-product-title'}).getText().strip()
        except:
            Title = ''
        try:
            Brand = getData('Brand:')
        except:
            Brand = ''
        try:
            Seller = soup.find(attrs = {'class':'more-from-brand'}).getText().replace('More From ','').strip()
        except:
            Seller = ''
        try:
            IMG_medium = soup.find(attrs = {'id':'vipImage'}).find('img')['src']
        except:
            IMG_medium = ''
        try:
            IMG_large = soup.find(attrs = {'id':'bigImageContainer'})['src']
        except:
            IMG_large = ''
        try:
            Price_mrp = soup.find(attrs = {'class':'vip-prices'}).findAll('li')[0].getText().strip().replace('"','').replace('Retail Price: Rs.','').replace(',','')
            Price_mrp = re.compile(r'(\d+)').search(Price_mrp).group(0)
        except:
            Price_mrp = ''
        try:
            Price_selling = re.findall(r'\d+', soup.find(attrs = {'class':'vip-prices'}).findAll('li')[1].getText().strip().replace(',','').replace('Offer Price:','').replace('Rs.','').replace(',',''))[0]
        except:
            Price_selling = Price_mrp

        if Price_mrp == '':
            Price_mrp = Price_selling

        try:
            pincode='110001'
            prc_code=soup.find(attrs = {'id':'cod_prc_code'})['value']#'4122' 
            sku= PID #'LL1375807-P-WH11390'
            supplier=soup.find(attrs = {'id':'cod_supplier_id'})['value'] #'1' #
            cod_exist=soup.find(attrs = {'id':'cod_open'})['value']#'0'#
            int_ship=soup.find(attrs = {'id':'int_ship'})['value']#'0'#
            brand_id=soup.find(attrs = {'id':'brand_id'})['value']#'3155'#
            assembly_check=soup.find(attrs = {'id':'assembly_check'})['value']#'0'#
            product_id=soup.find(attrs = {'id':'product_id'})['value']#'1375807'#
            is_customized='0'
            customized_id='0'
            ccid=re.findall('var\sccid\s=\s\"(.*?)\";', html)[0]#'2757' #
            uu = 'https://www.pepperfry.com/pincode/is_product_serviceable'
            data = {'pincode':pincode,'prc_code':prc_code,'sku':sku, 'supplier':supplier ,'cod_exist':cod_exist,\
                    'int_ship':int_ship, 'brand_id':brand_id, 'assembly_check':assembly_check, 'product_id':product_id,\
                    'is_customized':is_customized,'customized_id':customized_id ,'ccid':ccid}
            resp = requests.post(uu, data = data)
            data = dict(eval(resp.content.replace('true', 'True').replace('false','False')))

            try:
                COD = data['cod']
            except:
                COD = ''

            try:
                Delivery = data['tentative_delivery_date']
            except:
                Delivery = ''
            
        except:
            pass
        try:
            Price_shipping = soup.find(attrs = {'class':'tdcolor1'}).getText()
        except:
            Price_shipping = ''
        try:
            soup.find(attrs = {'id':'emi_strip'})
            EMI = 'Available'
        except:
            EMI = ''
        try:
            breadcrums = soup.find(attrs = {'class':'breadcrumb container'}).find(attrs = {'class':'cat_tree'}).findAll('span')
            b = ''
            for bread in breadcrums:
                try:
                    b = b + '|' + bread.find('span').getText().strip()
                except:
                    pass
            Category_path = b[1:].strip()
        except:
            Category_path = ''
        try:
            Description = soup.find(attrs = {'class':'vip-dtl-para'}).getText().strip()
        except:
            Description = ''

        try:
            Offers = soup.find(attrs = {'class':'vip-offer-text'}).getText()
        except:
            try:
                Offers = soup.find(attrs = {'class':'vip-cpn-box'}).getText()
            except:
                Offers = ''
        try:
            Average_rating = soup.find(attrs = {'class':'rating-text'}).getText()
        except:
            Average_rating = ''
        Reviews = ''
        try:
            if 'THIS ITEM IS SOLD OUT!' in str(soup):
                Status = 'OUT OF STOCK'
            else:
                Status = 'IN STOCK'
        except:
            Status = 'IN STOCK'

        Condition = 'NEW'
        TimeStamp = str(datetime.now())

        nrow = df.shape[0]
        df.loc[nrow+1] = [PID, URL_raw, Title, Brand,Seller, IMG_medium, IMG_large, Price_mrp, Price_selling, Price_shipping, Delivery,\
                          COD,EMI, Category_path,Description,Offers,Average_rating,Reviews,Status,Condition,TimeStamp]

        return df
