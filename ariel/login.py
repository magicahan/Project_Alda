import requests
import getpass
from util import *
from selenium import webdriver
from selenium.webdriver.support.ui import Select

def login():
	username = input('What is your uchicago ID: ')
	password = getpass.getpass(prompt = 'And your password: ')

	inputURL = "https://aisweb.uchicago.edu/psp/ihprd_newwin/EMPLOYEE/"+\
	"HRMS/c/UC_STUDENT_RECORDS_FL.UC_SSR_CLSRCH_FL.GBL?SC_ID=UC_S201607121025503472596999"

	browser = webdriver.Firefox()
	browser.implicitly_wait(5)
	print('browser ready')
	browser.get(inputURL)
	browser.find_element_by_name('j_username').send_keys(username)
	browser.find_element_by_name('j_password').send_keys(password)
	login_form = browser.find_element_by_name('_eventId_proceed')
	login_form.click()
	print("Now you're on UC classes page")
	return(browser)
	# r = get_request(inputURL)
	# loginURL = get_request_url(r)

	# with requests.Session() as s:
	# 	p = s.post(loginURL, data = {'j_username': username, 'j_password': password})
	# 	print(p)
	# 	print(p.text)


# def scrapper(browser):
# 	quarter = browser.find_element_by_xpath('//select[@id="UC_CLSRCH_WRK2_STRM"]/option[@value="2174"]')
# 	quarter.



if __name__ == "__main__":
	browser = login()
	# scrapper(browser)

