from selenium import webdriver
driver = webdriver.Firefox()

email = 'hagelbakaler@yahoo.com'
username = 'hagelbakaler@yahoo.com' 
password = 'PaEqcRyGuk3374'
driver.get('https://www.fiverr.com/')
driver.find_element_by_css_selector('.js-open-popup-join.js-gtm-event').click()
email = driver.find_element_by_css_selector('.js-form-email').send_keys(email)
driver.find_element_by_id('join-btn').click()
                                                                                                                                                                                                                                                                                                                                                                                                                     
username = driver.find_element_by_css_selector('.js-form-username')
username.send_keys(username)
password = driver.find_element_by_css_selector('.js-form-password')
password.send_keys(password)
driver.find_element_by_id('join-btn').click()
