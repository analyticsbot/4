from selenium import webdriver
import time
import pandas as pd
import re

driver = webdriver.Firefox()

group_url = 'https://www.facebook.com/groups/kmarie0308/'

driver.get("https://www.facebook.com/")
driver.find_element_by_id("email").clear()
driver.find_element_by_id("email").send_keys("hari.shankar2390@gmail.com")
driver.find_element_by_id("pass").clear()
driver.find_element_by_id("pass").send_keys("ravihari!12")
driver.find_element_by_id("pass").submit()
#driver.find_element_by_id("u_0_4").click()

time.sleep(5)

driver.get(group_url)
time.sleep(2)
f = driver.find_element_by_id('pagelet_group_profile_members').find_element_by_link_text('See All')

url = f.get_attribute('href')
driver.get(url)
time.sleep(3)

len_profiles = [1,3,4]

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    x=driver.find_elements_by_css_selector('.fbProfileBrowserListItem')
    len_profiles.append(len(x))
    if len_profiles[-1] == len_profiles[-2]:
        break

count = 0
for i in x:
    name = i.find_element_by_id('js_i').text
    occupation = i.text.split('\n')[1]
    added = i.text.split('\n')[2]
    profile_url = i.find_element_by_id('js_i').get_attribute('data-hovercard')
    id = re.findall(r'id=(.*?)&', profile_url)[0]
    print name, occupation, added, profile_url, id
    count+=1
    if count==5:
        break
    
