# -*- coding: utf-8 -*-
"""
Created on Mon Feb 08 10:17:57 2016

@author: Dean
"""
from __future__ import division
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import pandas as pd
import time
print time.ctime()
import urlparse
from time import strptime
import datetime
import hashlib

urls = ['http://www.oddsportal.com/hockey/finland/liiga/results/#/page/']
#driver = webdriver.PhantomJS(executable_path=r'C:/phantomjs.exe')
driver = webdriver.Firefox()
filename = 'finland_liiga.csv'
try:
    df = pd.read_csv(filename)
    df_exists = True
except:
    df_exists = False

print df.shape
        
# put this link in your browser to see upcoming games: http://www.oddsportal.com/hockey/finland/liiga/
# another example here: http://www.oddsportal.com/hockey/usa/nhl/

def get_next(urls, csvname, df, max_page=1):
    upcoming = [w.split('/results/#/page/')[0] for w in urls]
    data = []    
    
    def country_assigner(url):
        parsed = urlparse.urlparse(url)
        
        country = parsed.path.rsplit("/")[2]
        
        if "switzerland/nlb" in url:
            country = 'switzerland2'
            return country
        elif "sweden/hockeyallsvenskan" in url:
            country = 'sweden2' 
            return country
        elif "germany/del2" in url:
            country = 'germany2'
            return country
        elif "finland/mestis" in url:
            country = 'finland2'
            return country
        else:
            return country
            
    def parse(url, pos):
        parsed = urlparse.urlparse(url)
        return parsed.path.rsplit("/")[pos] 
    
    for url in urls:
        for page in range(1,max_page):
            
            driver.implicitly_wait(10)
            wait = WebDriverWait(driver, 10)        
            print url + str(page)        
            driver.get(url + str(page))
            # wait for the page to load
            try:     
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div#tournamentTable tr.deactivate")))
            
            except TimeoutException:
                break
            
            for match in driver.find_elements_by_css_selector("div#tournamentTable tr.deactivate"):
                home, away = match.find_element_by_class_name("table-participant").text.split(" - ")
                date = match.find_element_by_xpath(".//preceding::th[contains(@class, 'first2')][1]").text
                a, b, c = match.find_elements_by_class_name("odds-nowrp")
                score = match.find_element_by_class_name("table-score").text    
                if ":" not in score:
                    hg = "-1"
                    ag = "-1"
                else:                
                    hg, ag = score.split(":")  
                    if " " in ag:                
                        ag, txt_ev = ag.split(" ")
    
                    else:
                        txt_ev = np.nan           
                
                if "oday" in date:
                    date = datetime.date.today().strftime("%d %b %Y")
                    event = "Not specified"

                elif "esterday" in date:
                    date = datetime.date.today() + datetime.timedelta(days=-1)
                    date = date.strftime("%d %b %Y")                
                    event = "Not specified"                
                elif " - " in date:
                    date, event = date.split(" - ")
                    
                else:
                    event = "Not specified"

                item_to_be_hashed = str(home.strip())+str(away.strip())+str(date.strip())+str(hg.strip())+str(ag.strip())+str(event.strip())+\
                                 str(txt_ev)+str(a.text)+ str(b.text)+str(c.text)+str(country_assigner(url))+str(parse(url, 3))
                hash_value = hashlib.md5(item_to_be_hashed).hexdigest()
                if df_exists:
                    if df.query('hash_value == "' + hash_value + '"').shape[0] == 0:
                        data.append({
                            "home": home.strip(),
                            "away": away.strip(),
                            "date": date.strip(),
                            "home_score": hg.strip(),
                            "away_score": ag.strip(),
                            "event": event.strip(),
                            "decision" : txt_ev,
                            "h_odds": a.text,
                            "x_odds": b.text,
                            "a_odds": c.text,
                            "url": url,
                            "country": country_assigner(url),
                            "league": parse(url, 3)
            
                        })
                else:
                    data.append({
                            "home": home.strip(),
                            "away": away.strip(),
                            "date": date.strip(),
                            "home_score": hg.strip(),
                            "away_score": ag.strip(),
                            "event": event.strip(),
                            "decision" : txt_ev,
                            "h_odds": a.text,
                            "x_odds": b.text,
                            "a_odds": c.text,
                            "url": url,
                            "country": country_assigner(url),
                            "league": parse(url, 3)
            
                        })
                        
    
            print len(data)
    
    for url in upcoming:    
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver, 10)        
        print url# + str(page)        
        driver.get(url) # + str(page))
        # wait for the page to load
        try:     
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table#tournamentTable tr.odd")))        
        except TimeoutException:
            continue
        
        for match in driver.find_element_by_css_selector("table#tournamentTable").find_elements_by_tag_name('tr'):
            try:
                home, away = match.find_element_by_class_name("table-participant").text.split(" - ")
                date = match.find_element_by_xpath(".//preceding::th[contains(@class, 'first2')][1]").text
                a, b, c = match.find_elements_by_class_name("odds-nowrp")

                if "oday" in date:
                    date = datetime.date.today().strftime("%d %b %Y")
                    event = "Not specified"

                elif "omorrow" in date:
                    date = datetime.date.today() + datetime.timedelta(days=1)
                    date = date.strftime("%d %b %Y")                
                    #date = date.str
                    event = "Not specified"
                    
                elif "esterday" in date:
                    date = datetime.date.today() + datetime.timedelta(days=-1)
                    date = date.strftime("%d %b %Y")                
                    #date = date.str
                    event = "Not specified"                
                elif " - " in date:
                    date, event = date.split(" - ")
                    
                else:
                    event = "Not specified"
                item_to_be_hashed = str(home.strip())+str(away.strip())+str(date.strip())+str(event.strip())+\
                                     str(a.text)+ str(b.text)+str(c.text)+str(country_assigner(url))+str(parse(url, 3))
                hash_value = hashlib.md5(item_to_be_hashed).hexdigest()
                if df_exists:
                        if df.query('hash_value == "' + hash_value + '"').shape[0] == 0:
                            data.append({
                                "home": home.strip(),
                                "away": away.strip(),
                                "date": date,#.strip(),
                                #"home_score": hg.strip(),
                                #"away_score": ag.strip(),
                                "event": event.strip(),
                                #"decision" : txt_ev,
                                "h_odds": a.text,
                                "x_odds": b.text,
                                "a_odds": c.text,
                                "url": url + str('/results/#/page/'),
                                "country": country_assigner(url),
                                "league": parse(url, 3),
                                "home_score": np.nan,
                                "away_score": np.nan
                            })
                else:
                    data.append({
                                "home": home.strip(),
                                "away": away.strip(),
                                "date": date,#.strip(),
                                #"home_score": hg.strip(),
                                #"away_score": ag.strip(),
                                "event": event.strip(),
                                #"decision" : txt_ev,
                                "h_odds": a.text,
                                "x_odds": b.text,
                                "a_odds": c.text,
                                "url": url + str('/results/#/page/'),
                                "country": country_assigner(url),
                                "league": parse(url, 3),
                                "home_score": np.nan,
                                "away_score": np.nan
                            })
            except:
                pass
    
        #driver.close()
        print len(data)
    
    def clean(s):
        try:
            s = float(s)        
            if s > 99:
                return 1 + (s / 100)
            elif s < -99:
                return  1 + (100 / -s)
            else:
                return s

        except ValueError:
           
            if "-" in s:
                try:            
                    m, p = s.split('-')
                    m = int(m)
                    p = strptime(p,'%b').tm_mon
                    p = int(p)
                    #print m, p
                    return 1 + (p / m)
                except:
                    p, m = s.split('-')
                    m = int(m)
                    p = strptime(p,'%b').tm_mon
                    p = int(p)
                    #print m, p
                    return 1 + (p / m)
            else:
                       
                n, d = s.split('/')
                n = int(n) ,
                d = int(d)
                return 1 + (n[0] / d)
                

    if not df_exists:
        df = pd.DataFrame(data)
        df['h_odds'] = df.h_odds.map(clean)
        df['x_odds'] = df.x_odds.map(clean)
        df['a_odds'] = df.a_odds.map(clean)
    else:
        temp = pd.DataFrame(data)
        temp['h_odds'] = df.h_odds.map(clean)
        temp['x_odds'] = df.x_odds.map(clean)
        temp['a_odds'] = df.a_odds.map(clean)
        df = pd.concat([df, temp], axis = 0)    
    
    print time.ctime()
    print df.shape
    
    df.to_csv(csvname)
    return df

get_next(urls, 'finland_liiga.csv', df)
driver.close() 
