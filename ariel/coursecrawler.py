import requests
# import getpass
# from util import *
# import bs4
from selenium import webdriver
from selenium.webdriver.support.ui import Select


def find_dept_ls(course_url):
	driver = webdriver.PhantomJS()
	driver.implicitly_wait(10)
	driver.set_window_size(1024,768)
	driver.get(course_url)

	quarter_select = Select(driver.find_element_by_id('UC_CLSRCH_WRK2_STRM'))
	if quarter_select.first_selected_option.text != 'Spring 2017':
		quarter_select.select_by_value('2174')
	# driver.save_screenshot('screen.png')
	driver.implicitly_wait(20)

	dept_select = Select(driver.find_element_by_id('UC_CLSRCH_WRK2_SUBJECT'))
	depts = dept_select.options
	dept_ls = []
	for i in depts[1:]:
		dept_ls.append(i.get_attribute('value'))

	return (dept_select, dept_ls, driver)


def one_page_crawler(results_one_page, driver, courses_dict):
	for i in range(results_one_page):
		coursechunk = 'DESCR100$0_row_' + str(i)
		driver.find_element_by_id(coursechunk).click()
		driver.implicitly_wait(30)
		driver.save_screenshot('screen.png')
		coursekey = driver.find_element_by_id('win0divUC_CLS_DTL_WRK_HTMLAREA$0')
		coursekey = coursekey.text.split()
		coursename = driver.find_element_by_id('UC_CLS_DTL_WRK_UC_CLASS_TITLE$0')
		coursename = coursename.text
		coursedscp = driver.find_element_by_id('UC_CLS_DTL_WRK_DESCRLONG$0')
		coursedscp = coursedscp.text
		instructors = driver.find_element_by_id('MTG$0').text
		daytime = driver.find_element_by_id('MTG_SCHED$0').text
		loc = driver.find_element_by_id('MTG_LOC$0').text
		career = driver.find_element_by_id('PSXLATITEM_XLATLONGNAME$33$$0').text
		
		courseid = coursekey[0] + coursekey[1][:-2]
		section = coursekey[1][-1]
		sectionid = coursekey[2]
		coursetype = coursekey[4]
		courses_dict[courseid] = dict()
		courses_dict[courseid]['name'] = coursename
		courses_dict[courseid]['section'] = section
		courses_dict[courseid]['sectionid'] = sectionid
		courses_dict[courseid]['type'] = coursetype
		courses_dict[courseid]['instructor'] = instructors
		courses_dict[courseid]['location'] = loc
		courses_dict[courseid]['daytime'] = daytime
		courses_dict[courseid]['career'] = career
		courses_dict[courseid]['description'] = coursedscp

		sub = driver.find_element_by_id('win0divUC_CLS_REL_WRK_RELATE_CLASS_NBR_1$373$$0').text
		if len(sub) != 0:
			courses_dict[courseid]['subsections'] = list()
			subcounts = len(driver.find_elements_by_id("win0divSSR_CLS_TBL_R11$grid$0"))
			for i in range(subcounts):
				courses_dict[courseid]['subsections'].append(dict())
				subkey = driver.find_element_by_id('win0divDISC_HTM$' + str(i)).text
				subinstructor = driver.find_element_by_id('win0divDISC_INSTR$' + str(i)).text
				subtime = driver.find_element_by_id('DISC_SCHED$' + str(i)).text
				courses_dict[courseid]['subsections'][i]['sectionname'] = subkey
				courses_dict[courseid]['subsections'][i]['sectionname'] = subkey
				courses_dict[courseid]['subsections'][i]['sectionname'] = subkey
		else:
			courses_dict[courseid]['subsections'] = []

		returnid = 'UC_CLS_DTL_WRK_RETURN_PB$0'
		driver.find_element_by_id(returnid).click()

	return courses_dict


def one_dept_crawler(dept_select, dept, driver, searchbutton, courses_dict):
	dept_select.select_by_value(dept)
	searchbutton.click()
	resultsize = driver.find_element_by_id('UC_RSLT_NAV_WRK_PTPG_ROWS_GRID').text.split()[0]
	resultsize = int(resultsize)
	pages = 1
	if resultsize > 25:
		pages = resultsize // 25 + 1

	while pages > 1:
		results_one_page = 25
		one_page_crawler()
		# then click next page
		pages = pages - 1

	# elif pages = 1:
	# 	results_one_page = resultsize % 25
	# 	one_page_crawler()
		





def course_crawler(dept_select, dept_ls, driver):
	searchbutton = driver.find_element_by_id('UC_CLSRCH_WRK2_SEARCH_BTN')
	for dept in dept_ls:
		dept_select.select_by_value(dept)
		searchbutton.click()










if __name__ == "__main__":
	course_url = 'https://coursesearch.uchicago.edu/psc/prdguest/EMPLOYEE/HRMS/c/UC_STUDENT_RECORDS_FL.UC_CLASS_SEARCH_FL.GBL'

	courses_dict = dict()
	dept_select, dept_ls, driver = find_dept_ls(course_url)

	driver.implicitly_wait(10)
	driver.save_screenshot('screen0.png')
	searchbutton = driver.find_element_by_id('UC_CLSRCH_WRK2_SEARCH_BTN')

	dept_select.select_by_value(dept_ls[0])

	searchbutton.click()
	driver.implicitly_wait(10)
	driver.save_screenshot('screen1.png')

	resultsize = driver.find_element_by_id('UC_RSLT_NAV_WRK_PTPG_ROWS_GRID').text.split()[0]

	resultsize = int(resultsize)

	testdic = one_page_crawler(resultsize, driver, courses_dict)

	driver.quit()
