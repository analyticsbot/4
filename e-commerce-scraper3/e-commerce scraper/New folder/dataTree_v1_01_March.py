# import all required modules
from selenium import webdriver
import time, re, hashlib, csv
import pandas as pd
from selenium.webdriver.common.keys import Keys
import usaddress
import logging, datetime, sys
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.ERROR)

# log file initialize
logging.basicConfig(level=logging.DEBUG, 
                    filename='logfile3.log', # log to this file
                    format='%(asctime)s -- %(message)s') # include timestamp
headers = ['Date' , 'Client_Name', 'State', 'County', 'searchterm', 'recordyear', 'Doctypes', 'Records_Count', 'last data record found', 'parsed_rows']

ignore_keywords = ['escrow', 'law', 'associates', 'recorder', 'recorders', '$' , 'iiii', 'service', 'closing', 'title']
logging.info("Sentences will following keywords will be ignored -- " + ', '.join(ignore_keywords))
try:
    writer = pd.ExcelWriter('client_log.xlsx')
    df_data = pd.read_excel('client_log.xlsx','Sheet1')
    print("Opened the client log file. Read the contents into a dataframe!")
except:
    writer = pd.ExcelWriter('client_log.xlsx', engine='xlsxwriter')
    cols_data = headers
    df_data = pd.DataFrame(columns=cols_data)
# static variables
url_login = 'https://web.datatree.com/Account/Login?ReturnUrl=%2f'
username = 'Allenbruns'
pwd = 'billie54'
state = 'CA'
county = 'ORANGE'
keyword = '"mail to"'
input_file_name = ''
output_file_name = 'datatree3.csv'

salutation = '' #Mr. Miss
client_name = ''
client_address = ''
billing_card_number = ''
card_cvv_number = ''
billing_address = ''
billing_expiry_date = ''

logging.info("Process started for " + salutation  + ' ' +client_name + ', address = '+ client_address)
logging.info("Billing details, billing_card_number = " + billing_card_number  + ', card_cvv_number: ' +card_cvv_number + \
             ', billing_address = '+ billing_address + ', billing_expiry_date = ' + billing_expiry_date)

try:
    df_past = pd.read_csv(input_file_name)
    logging.info("Successfully read last file : " + input_file_name)
except:
    df_past = False
    logging.error("Cannot read last file : " + input_file_name)

doc_types = ['POWER OF ATTORNEY']
"""
POSSIBLE VALUES
['UNDETERMINED', 'DEED', 'DEED OF TRUST', 'RELEASE', 'ABSTRACT OF JUDGMENT', 'FEDERAL LIEN', 'SUBSTITUTION', 'NOTICE OF DEFAULT', 'LIEN', 'NOTICE', 'AFFIDAVIT OF DEATH', 'TRUST', 'ORDER', 'POWER OF ATTORNEY', 'ASSESSMENT LIEN', 'STATE LIEN', 'RESCISSION', 'ASSIGNMENT', 'SUBSTITUTION & RELEASE', 'RESTRICTIONS', 'FINANCING STATEMENT', 'AGREEMENT', 'EASEMENT', 'SUBORDINATION', 'AFFIDAVIT', 'CERTIFICATE', 'MORTGAGE', 'MODIFICATION', 'ACKNOWLEDGEMENT', 'PARTIAL RELEASE', 'LIS PENDENS', 'BUSINESS', 'JUDGMENT', 'DECLARATION', 'SURVEY', 'SATISFACTION', 'MECHANICS LIEN', 'ASSIGNMENT OF RENTS', 'REQUEST', 'RIDER', 'SALE', 'CONDOMINIUM', 'NOTE', 'MINERAL/MINING CLAIM', 'HOMESTEAD', 'BOND', 'LICENSE', 'WITHDRAWAL', 'SUBSTITUTION & PARTIAL', 'REVOCATION', 'PROBATE', 'NOTICE OF TRUSTEES SALE', 'DEATH CERTIFICATE', 'BANKRUPTCY', 'CONTRACT', 'ANNEXATION', 'AMENDMENT', 'OPTION', 'MORTGAGE/DEED OF TRUST', 'MEMORANDUM', 'INDENTURE', 'FORECLOSURE', 'CIVIL ACTION', 'APPLICATION', 'TERMINATION', 'RESOLUTION', 'PETITION', 'PARTIAL ASSIGNMENT', 'CANCELLATION', 'ABANDONMENT']
"""

years = ['2016']
"""POSSIBLE VALUES
['2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000']
"""

logging.info("Starting the process. Variables are state = " + state + ", county = " + county + ",keyword = " + keyword + \
             ", document types selected are " + '; '.join(doc_types) + ", for year(s)" + '; '.join(years))

# initialize pandas
df = pd.DataFrame(columns = ['date', 'text_box_left','DOCUMENT_TYPE', 'RECORDING_DATE', 'APN', \
                             'ADDRESS', 'OWNER_BORROWER','SELLER_LENDER', 'text',\
                             'parsed_name_address', 'parsed_name', 'parsed_address',\
                             'streetName','StreetNamePostType', 'PlaceName', 'StateName',\
                             'ZipCode','StreetNamePostType', 'StreetNamePreDirectional', 'hash_value', 'is_parsed'])

# start the firefox instance
driver = webdriver.Firefox()
driver.maximize_window()
driver.get(url_login)

# username handling on the website
username_elem = driver.find_element_by_id('UserName')
username_elem.send_keys(username)

# password handling
pwd_elem = driver.find_element_by_id('Password')
pwd_elem.send_keys(pwd)

# press enter to login
pwd_elem.submit()

logging.info("Successfully logged into account : " + username)

# waiting for 5 second before proceeding
time.sleep(5)
flexi_search_url = 'https://web.datatree.com/flexsearch'
driver.get(flexi_search_url)

# waiting for 5 second before proceeding
time.sleep(5)
driver.find_element_by_name('Advanced').click()

query = '(state:"' + state + '") AND (doc_full_text:' + keyword + \
        ') AND (county:"' + county + '") '
for doc in doc_types:
    query += ' AND (doc_type_search:'  + ' AND doc_type_search:'.join(doc.split())+ ') '

if len(years)>0:
    query += ' AND '
    
for yr in years:
    query += ' (year:' + str(yr) + ') OR '

query =  query[:-3].strip()

logging.info("Query for this search : " + query)
             
textarea = driver.find_element_by_xpath('//*[@id="flex"]/ng-switch/advanced-flex-search/div/div[3]/div/textarea')
textarea.send_keys(query)
driver.find_element_by_css_selector('.runflexsrch-btncntnr').click()

time.sleep(30)
logging.info("Starting parsing data")
count = 0
post_count = 0
hash_value = [1,2,3]
cur_date = str(datetime.datetime.now().strftime ("%Y-%m-%d"))
text_box_left = ''
while True:
    if count == 0:
        count +=1
        logging.info("Parsing page 0")
    else:
        next_ = driver.find_element_by_css_selector('li.ng-scope:nth-child(11) > a:nth-child(1)')
        next_.click()
        logging.info("Parsing page "+  str(count))
        count +=1
        if hash_value[-1] == hash_value[-2]:
            logging.info("No next page exists. Exiting")
            break
    try:        
        time.sleep(10)
        results =  driver.find_elements_by_id('flexSearchResults')
        time.sleep(10)
        try:
            driver.execute_script("return arguments[0].scrollIntoView();", results[0])
        except:
            pass
        time.sleep(10)
        for result in results:
            if (results.index(result)+1) %2 == 0:
                driver.execute_script("return arguments[0].scrollIntoView();", result)
                time.sleep(1)
            try:
                text_box_left = result.find_element_by_css_selector('.col-md-10.flexsearch-highlights').text
            except:
                text_box_left = 'NA'
            if results.index(result) == len(results)-1:
                hash_value.append(hashlib.md5(text_box_left).hexdigest())
            try:
                x = result.find_elements_by_css_selector('.doc-data-style.ng-binding')
            except:
                pass
            try:
                DOCUMENT_TYPE = x[0].text
            except:
                DOCUMENT_TYPE = 'NA'
            try:
                RECORDING_DATE = x[1].text
            except:
                RECORDING_DATE = 'NA'
            try:
                APN = x[2].text
            except:
                APN = 'NA'
            try:
                ADDRESS = x[3].text
            except:
                ADDRESS = 'NA'
            try:
                OWNER_BORROWER = x[4].text
            except:
                OWNER_BORROWER = 'NA'
            try:
                SELLER_LENDER = x[5].text
            except:
                SELLER_LENDER = 'NA'
    
            if not any(word in text_box_left for word in ignore_keywords):
                try:
                    data_from_left = text_box_left.lower().split(keyword.replace('"',''))[1]
                    hash_left_data = hashlib.md5(text_box_left).hexdigest()
                    if df_past:
                        if df_past.query('hash_value == "' + hash_left_data + '"').shape[0] == 0:
                            logging.info("Found existing record. Exiting")
                            df.to_csv(output_file_name, index = False)
                            logging.info("Output written to file : ", output_file_name)
                            sys.exit(1)
                    
                    name_address = re.findall(r'\s([a-z][a-z]+.*?)$', data_from_left)[0]
                    name_address = re.findall(r'(\w\w.*?\s\w\w\.?\s*\d\d\d\d\d)', name_address)[0]
                    
                    name_address_split = name_address.split()
                    b = 0
                    for i in name_address_split:
                        b+=1
                        try:
                            i = int(i)
                            isinstance(i, int)
                            break
                        except Exception,e:
                            print 'aaa', str(e)
                    name = ' '.join(name_address_split[:b-1])
                    address = ' '.join(name_address_split[b-1:])
                    parse_address = usaddress.parse(address)
                    parse_address_dict = {}
                    for i in parse_address:
                        if i[1] not in parse_address_dict.keys():
                                parse_address_dict[i[1]] = i[0]
                        else:
                                parse_address_dict[i[1]] += ' '+ i[0]
                    try:
                        address_number = parse_address_dict['AddressNumber']
                    except:
                        address_number = 'NA'
                    try:
                        streetName = parse_address_dict['StreetName']
                    except:
                        streetName = 'NA'
                    try:
                        StreetNamePostType = parse_address_dict['StreetNamePostType']
                    except:
                        StreetNamePostType = 'NA'
                    try:
                        PlaceName = parse_address_dict['PlaceName']
                    except:
                        PlaceName = 'NA'
                    try:
                        StateName = parse_address_dict['StateName']
                    except:
                        StateName = 'NA'
                    try:
                        ZipCode = parse_address_dict['ZipCode']
                    except:
                        ZipCode = 'NA'
                    try:
                        StreetNamePostType = parse_address_dict['StreetNamePostType']
                    except:
                        StreetNamePostType = 'NA'
                    try:
                        StreetNamePreDirectional = parse_address_dict['StreetNamePreDirectional']
                    except:
                        StreetNamePreDirectional = 'NA'
                    is_parsed = 1
                except Exception,e:
                    print '111', str(e)
                    logging.error("Cant parse data for left hand side text -- " + data_from_left + '\n and hash value -- ' + \
                                 hash_left_data)
                    name = 'NA'
                    name_address = 'NA'
                    address = 'NA'
                    streetName='NA'
                    StreetNamePostType='NA'
                    PlaceName='NA'
                    StateName='NA'
                    ZipCode='NA'
                    StreetNamePostType='NA'
                    StreetNamePreDirectional='NA'
                    is_parsed = 0
                    data_from_left = text_box_left.lower().split(keyword.replace('"',''))[1]
            else:
                logging.info("Not parsing. Either escrow or law or recorder or associates present in the left hand side text -- " + data_from_left + '\n and hash value -- ' + \
                                 hash_left_data)
                name = 'NA'
                name_address = 'NA'
                address = 'NA'
                streetName='NA'
                StreetNamePostType='NA'
                PlaceName='NA'
                StateName='NA'
                ZipCode='NA'
                StreetNamePostType='NA'
                StreetNamePreDirectional='NA'
                is_parsed = 0
                data_from_left = text_box_left.lower().split(keyword.replace('"',''))[1]
            post_count +=1
            df.loc[post_count] = [cur_date, text_box_left, DOCUMENT_TYPE, RECORDING_DATE, APN, \
                                  ADDRESS, OWNER_BORROWER, SELLER_LENDER, data_from_left, name_address, name, address,\
                                  streetName, StreetNamePostType, PlaceName, StateName,\
                             ZipCode, StreetNamePostType, StreetNamePreDirectional, hash_left_data, is_parsed]
                
    except Exception,e:
        print '222', str(e)
nrow = df_data.shape[0]
parsed_rows_total = sum(list(df['is_parsed']))
df_data.loc[nrow+1] = [str(datetime.datetime.now()), username, state, county, keyword, ', '.join(years), ','.join(doc_types), df.shape[0], text_box_left,parsed_rows_total]
df_data.to_excel(writer,'Sheet1', index = False, header = headers)
writer.save()
logging.info("Client log file generated as excel")
logging.info("Total number of rows parsed successfully :: " + str(parsed_rows_total))
driver.close()
logging.info("Total pages scraped : " + str(count))
logging.info("Total records scraped : " +  str(df.shape[0]))
df.to_csv(output_file_name, index = True)
logging.info("Output written to file : " + output_file_name)
