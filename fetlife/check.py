import mechanize, datetime, time, sqlite3, sqlalchemy, re, argparse, logging, requests
from bs4 import BeautifulSoup
from text_unidecode import unidecode
import random,time,sys, shutil
from sqlalchemy import create_engine, MetaData

nickname = 'c1233645' ## login username to fetlife
password = 'facebook' ## password to fetlife for the above username
url = 'https://fetlife.com/countries/84/kinksters' ## url for which the profiles are to be scraped
mindelay = 1 ## minimum seconds to wait before scraping next profile
maxdelay = 3 ## maximum seconds to wait before scraping next profile
maxprofiles = 500 ## maximum profiles to be scraped before the script exits . 0 means go on indefenitly. 
newonly = 0 ## boolean field. 1 indicates scrape only new profiles. 0 means scrape and update exiting profiles too
maxtime = 100000 ## maxumum time in seconds for which the script should run before exiting. 0 means go forever
database = 'postgresql://postgres:postgres@localhost/fetlife' ## database connection url
debug = 1 ## whether to print output to screen
proxy = 0 ## whether to accept proxies

user_url = 'https://fetlife.com/users/1103243'
## intantiate the mechanize browser
br = mechanize.Browser()
br.set_handle_robots(False)
if proxy:
    br.set_proxies({"http": proxy})
br.open('https://fetlife.com/login')
br.select_form(nr=0)
br.form.new_control('text', 'nickname_or_email', {'value': nickname})
br.form.new_control('password', 'password', {'value': password})
resp = br.submit()

def downloadImage(url, name):
    response = requests.get(url, stream=True)
    with open(IMAGES_FOLDER+'//'+str(name)+'.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

def getElement(table, name):
    """ function to get the elements in tabular format
    table - all elements in table
    name - name of the element for which value is required
    """
    for el in table:
        try:
            if el.find('th').getText() == name:
                return el.find('td')
        except:
            return ''

def getBottomElement(bottom, name):
    """ function to get the bottom elements 
    bottom - all elements in bottom
    name - name of the element for which value is required
    """
    for b in bottom:
        try:
            if b.getText().strip() == name.strip():
                if name.strip() == 'Websites':
                    return b.findNextSibling().getText()
                elif name.strip() == 'Latest pictures':
                    pics = b.findNextSiblings('a')
                    value = ''
                    for p in pics:
                        value  = value + '; ' + p.find('img')['src']
                    return value
                elif name.strip() == 'About me':
                    value= ''
                    x = b.findNextSibling()
                    while True:
                        if x.name == 'p':
                            value += ' ' + x.getText()
                            x = x.findNextSibling()
                        else:
                            break
                    return value.strip().replace('\n',' ')
                
                value= ''
                ids = ''
                x = b.findNextSibling()
                while True:                    
                    if x.name == 'p':
                        value += ' ' + x.getText()
                        ids += ', ' + re.findall(r'\d+', x.find('a')['href'])[0]
                        x = x.findNextSibling()
                    else:
                        break
                return value.strip(), ids[1:].strip()
        except:
            return ''

def getListElement(listElem, name):
    """ function to get the elements in list format
    listElem - all elements in list
    name - name of the element for which value is required
    """
    ids = []
    try:
        for l in listElem:
            try:
                if l.findPreviousSibling().getText().strip() == name.strip():                
                    if name.strip() == 'Groups member of':
                        return l.getText().strip(), [re.findall(r'\d+',link['href'])[0] for link in l.findAll('a')]
                    else:
                        return l.getText().strip()
            except:
                return ''
    except:
        return ''

def getLookingForStatus(Looking_for_options, name):
    """ function to get the looking for values
    Looking_for_options - all looking for options
    name - name of the element for which value is required
    """
    try:
        if name in Looking_for_options:
            return True
        else:
            return False
    except:
        return False

def getDSRelationshipStatus(D_s_Relationships, name):
    """ function to get the D_s_Relationships values
    D_s_Relationships - all D_s_Relationships options
    name - name of the element for which value is required
    """
    returnValue = []
    try:
        for relation in D_s_Relationships:
            if relation.split()[-1].lower() != name.lower():
                returnValue.append(relation.split()[-1])
            else:
                returnValue.append('1')
##            else:
##                returnValue.append(['0', ''])
    except:
        returnValue.append(None)
    return returnValue

def checkDSRelationshipUnknown(D_s_Relationships, D_s_Relationships_values):
    if any(word in ' '.join(D_s_Relationships) for word in D_s_Relationships_values):
        return False
    else:
        return True

def checkRelationshipUnknown(Relationships, Relationships_values):
    if any(word in ' '.join(Relationships) for word in Relationships_values):
        return False
    else:
        return True

def getRelationshipStatus(Relationships, name):
    """ function to get the Relationships values
    Relationships - all Relationships options
    name - name of the element for which value is required
    """
    returnValue = []
    try:
        for relation in Relationships:
            if name in relation:
                if relation.split()[-1].lower() != name.lower():
                    returnValue.append(relation.split()[-1])
                else:
                    returnValue.append('1')
##            else:
##                returnValue.append(['0', ''])
    except:
        returnValue.append(None)
    return returnValue


br.open(user_url)
html = br.response().read()
soup = BeautifulSoup(html, 'lxml')
bottom = soup.findAll(attrs = {'class':'bottom'})
table = soup.findAll("tr")
listElem = soup.findAll(attrs={'class':'list'})
URL = 'https://fetlife.com/' + user_url
id_user = re.findall(r'\d+', user_url)[0]


