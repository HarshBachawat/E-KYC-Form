from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time

options = Options()
options.add_argument('--headless')

def has_connection(driver):
	try:
		driver.find_element_by_xpath('//span[@jsselect="heading" and @jsvalues=".innerHTML:msg"]')
		return False
	except: return True

	
def fill_form(fname,lname,father_name,gender,dob,aadhar_no,pan_no,city,state,pincode):
	dob = dob.replace('/','-')
	browser=webdriver.Chrome(executable_path='C:\\chromedriver.exe',chrome_options=options)
	browser.get('https://www.cognitoforms.com/VIT26/ekycapplicationform')
	if not has_connection(browser):
		print('No Internet Connection! Aborted')
		browser.quit()
		return 0
	s=browser.find_element_by_id('c-0-11')
	s.send_keys(fname)
	s=browser.find_element_by_id('c-1-10')
	s.send_keys(lname)
	s=browser.find_element_by_id('c-2-9')
	s.send_keys(father_name)
	s=Select(browser.find_element_by_id('c-3-8'))
	s.select_by_value(gender)
	s=browser.find_element_by_id('c-4-7')
	s.send_keys(dob)
	s=browser.find_element_by_id('c-5-6')
	s.send_keys(aadhar_no)
	s=browser.find_element_by_id('c-6-5')
	s.send_keys(pan_no)
	s=browser.find_element_by_id('c-7-4')
	s.send_keys(city)
	s=browser.find_element_by_id('c-8-3')
	s.send_keys(state)
	s=browser.find_element_by_id('c-9-2')
	s.send_keys(pincode)
	b=browser.find_element_by_id('c-submit-button')
	b.click()
	time.sleep(5)
	browser.quit()
	print('Form Filled Successfully')
	return 1

if __name__ == '__main__':
	fill_form('Abc','Xyz','Mno','Male','01/01/2020','4444 3333 2222','AZZBC1542W','Efg','Uvw','696969')