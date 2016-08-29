from selenium import webdriver
import time
import pandas as pd

f = open('doc_names.csv', 'rb')
doctor_names = f.read().split('\n')[:-1]
doctor_names = [d.strip().replace('"','') for d in doctor_names]

driver = webdriver.Firefox()
count = 0
df = pd.DataFrame(columns = ['email', 'last_name', 'first_name', 'speciality', 'state', 'university', 'profile_link'])
for doc in doctor_names:
    try:
        print count
        driver.get('https://www.bcm.edu/people')
        time.sleep(1)
        name =  driver.find_element_by_id('OrganizationName')
        name.send_keys(doc)
        last_name = doc.split(',')[0]
        first_name = doc.split(',')[1]
        btn = driver.find_element_by_css_selector('.btn.btn-inverse')
        btn.click()
        time.sleep(1)
        results = driver.find_element_by_class_name('find-results')
        profile_link = results.find_element_by_tag_name('a').get_attribute('href')
        link = results.find_element_by_tag_name('a')
        link.click()
        time.sleep(2)
        try:
            email  = driver.find_element_by_css_selector('.attribute.featured.email')
            email_add =  email.find_element_by_tag_name('a').text
        except:
            email_add = 'NA'
        try:
            Speciality = driver.find_element_by_css_selector('.job.division')
            speciality_ = Speciality.text
        except:
            speciality_ = 'NA'
        try:
            state = driver.find_element_by_css_selector('.city-state-zip')
            state_ = state.text
        except:
            state_ = 'NA'
        try:
            University = driver.find_element_by_css_selector('.job.organization')
            univer = University.text
        except:
            univer = 'NA'
        df.loc[count] = [email_add, last_name, first_name, speciality_, state_, univer, profile_link]
        count +=1
    except Exception,e:
            print doc, ' not found', str(e)
