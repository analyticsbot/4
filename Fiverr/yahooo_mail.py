from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

email = 'hagelbakaler@yahoo.com'
driver = webdriver.Firefox()
driver.get("https://login.yahoo.com")

logintxt = driver.find_element_by_name("username")
logintxt.send_keys(email)

pwdtxt = driver.find_element_by_name("passwd")
pwdtxt.send_keys(pwd)


button = driver.find_element_by_id("login-signin")
button.click()
driver.get("https://mail.yahoo.com")
print driver.current_url
