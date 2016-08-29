from selenium import webdriver
import time



driver = webdriver.Firefox()

url = 'https://findaphysician.bcm.edu/search/search'
driver.get(url)

a = driver.find_element_by_css_selector('.search_filter.col-sm-4.ng-scope')
a.click()

#Email, Last Name, First Name, Speciality, State, University
doctor_names = []
nxt = driver.find_elements_by_css_selector('.ng-scope.ng-binding')

count = 0
>>> docs = driver.find_element_by_class_name('search_filter_list').find_elements_by_class_name('ng-scope')
>>> for doc in docs:
            doctor_names.append(doc.text)


while True:
    try:
        if count !=0:
            nxt[count].click()
            time.sleep(5)
        docs = driver.find_element_by_class_name('search_filter_list').find_elements_by_class_name('ng-scope')

        for doc in docs:
            doctor_names.append(doc.text)

        if count == len(nxt):
            break
        count+=1
    except Exception,e:
        print str(e)


            
>>> len(doctor_names)
1151
>>> import csv
>>> f = open('doc_names.csv', 'wb')
>>> writer = csv.writer(f)
>>> for doc in doctor_names:
	writer.writerow([doc])

	
>>> f.close()
>>> driver.get('https://www.bcm.edu/people')


>>> doc
u'Ayyar, Lakshmy'
>>> name =  driver.find_element_by_id('OrganizationName')
>>> name.send_keys(doc)
>>> btn = driver.find_element_by_css_selector('.btn.btn-inverse')
>>> btn.click()
>>> results = driver.find_element_by_class_name('find-results')
>>> link = results.find_element_by_tag_name('a').get_attribute('href')
>>> link
u'https://www.bcm.edu/people/view/lakshmy-ayyar-m-b-b-s-m-d/b15e10e5-ffed-11e2-be68-080027880ca6'
>>> link = results.find_element_by_tag_name('a')
>>> link.click()
>>> #Email, Last Name, First Name, Speciality, State, University
>>> email  = driver.find_element_by_css_selector('.attribute.featured.email')
>>> email.text
u'Email\nayyar@bcm.edu'
>>> email.find_element_by_tag_name('a')
<selenium.webdriver.remote.webelement.WebElement object at 0x031D7F90>
>>> email.find_element_by_tag_name('a').text
u'ayyar@bcm.edu'
>>> Speciality = driver.find_element_by_css_selector('.job.division')
>>> Speciality.text
u'Pulmonary, Critical Care & Sleep Medicine'
>>> state = driver.find_element_by_css_selector('city-state-zip')

>>> state = driver.find_element_by_css_selector('.city-state-zip')
>>> state.text
u'Houston, Texas 77025'
>>> University = driver.find_element_by_css_selector('.job.organization')
>>> University.text
u'Baylor College of Medicine'



>>> df = pd.DataFrame(columns = ['email', 'last_name', 'first_name', 'speciality', 'state', 'university', 'profile_link'])
>>> for doc in doctor_names:
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
		email  = driver.find_element_by_css_selector('.attribute.featured.email')
		email_add =  email.find_element_by_tag_name('a').text
		Speciality = driver.find_element_by_css_selector('.job.division')
		speciality_ = Speciality.text
		state = driver.find_element_by_css_selector('.city-state-zip')
		state_ = state.text
		University = driver.find_element_by_css_selector('.job.organization')
		univer = University.text
		df.loc[count] = [email_add, last_name, first_name, speciality_, state_, univer, profile_link]
		count +=1
	except Exception,e:
		print doc, ' not found', str(e)







