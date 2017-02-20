#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 22:22:34 2017

@author: luxihan
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import bs4
import getpass
import json
import time
import signal
import csv


#### Time Out Handler#####
def signal_handler(signum, frame):
    raise Exception("Timeout!")

signal.signal(signal.SIGALRM, signal_handler)
############################

###Scraping Functions#########
def log_in(driver, eval_url):
    driver.implicitly_wait(10)
    username_field = driver.find_element_by_id('username')
    password_field = driver.find_element_by_id('password')
    user_name = input('Username: ')
    password = getpass.getpass("Password: ")
    print('Username: {} password received!'.format(user_name))
    username_field.send_keys(user_name)
    password_field.send_keys(password)
    submit_field = driver.find_element_by_xpath("//button[@type = 'submit']")
    submit_field.click()
    cookie_dict = driver.get_cookies()
    while len(cookie_dict) > 2:
        cookie_dict = driver.get_cookies()
    cookie = {i['name'] : i['value'] for i in cookie_dict}
    return cookie


def get_request(eval_url, cookie, search_terms = None):
    session = requests.Session()
    if search_terms != None:
        while True:
            signal.alarm(5)
            try:
                req = session.get(eval_url + 'index.php', params = search_terms,\
                                 cookies = cookie.copy())
                
            except:
                print('Connection Error.... Retry')
                signal.alarm(0)
                time.sleep(0.5)
                continue
            else:
                signal.alarm(0)
                break
    else:
        while True:
            signal.alarm(5)
            try:
                req = session.get(eval_url, cookies = cookie.copy())
            except:
                print('Connection Error.... Retry')
                signal.alarm(0)
                time.sleep(0.5)
                continue
            else:
                signal.alarm(0)
                break
        
    page = bs4.BeautifulSoup(req.content, "lxml")
    return req, page

#req = session.get(eval_url, cookies = cookie)

def find_dept_year_list(eval_url, cookie):
    req, page = get_request(eval_url, cookie)
    dept_list = page.find_all('select', attrs = {'id' : 'department', 'name' : 'Department'})
    dept = dept_list[0]
    opt = dept.find_all('option')
    dept_list = []
    for i in opt:
        if i.text == 'Department':
            continue
        else:
            dept_list.append(i['value'])

    year_list = page.find_all('select', attrs = {'id' : 'AcademicYear', 'name' : 'AcademicYear'})
    year = year_list[0]
    opt = year.find_all('option')
    year_list = []
    for i in opt:
        if i.text == 'Academic Year':
            continue
        else:
            year_list.append(i['value'])
    return dept_list, year_list


def compile_course_num(eval_url, cookie, dept_list, year_list):
#    dept_list = ['MATH']
    course_num_set = set()
    course_num_dict = {}    
    for i, dept in enumerate(dept_list):
        for year in year_list:
#            print("At the {}th department {}, year{}".format(i, dept, year))
            search_terms = {'Department': dept, 'AcademicYear': year,\
                            'EvalSearchType':'option-dept-search'}
#            time.sleep(0.1)
            cur_req, cur_page = get_request(eval_url, cookie, search_terms)
            table = cur_page.find('tbody')
            if table == None:
                continue
            rows = table.find_all('tr')
            for row in rows:
                course_num = row.find_all('td')[0].text
                course_num = ' '.join(course_num.split()[0:2])
                course_num_set.add(course_num)
        print("At the {}th department {}, year{}".format(i, dept, year))
    course_num_list = sorted(list(course_num_set))
    count = 0
    for course in course_num_list:
        count += 1
        course_num_dict[course] = count
    return course_num_dict


def compile_instructor_num(eval_url, cookie, dept_list, year_list):
    instructor_num_set = set()
    instructor_num_dict = {}
    for i, dept in enumerate(dept_list):
        for year in year_list:
            print("At the {}th department {}, year{}".format(i, dept, year))
            search_terms = {'Department': dept, 'AcademicYear': year,\
                            'EvalSearchType':'option-dept-search'}
            cur_req, cur_page = get_request(eval_url, cookie, search_terms)
            table = cur_page.find('tbody')
            if table == None:
                continue
            rows = table.find_all('tr')
            for row in rows:
#                time.sleep(0.3)
#                start = time.time()
                new_url = eval_url + row.find('a')['href']
                new_req, new_page = get_request(new_url, cookie)
#                print("load the page", time.time() - start)
                page_paragraph = new_page.find('p')
                if page_paragraph != None:
                    if len(page_paragraph.contents)>1:
                        instructors = str(new_page.find('p').contents[2])
                        instructor_list = instructors.split(';')
                    # avoid evluation not found
                    else:
                        instructors = row.find_all('td')[2].text
                        instructor_list = instructors.split(';')
                ## if the evluation page is blank
                else:
                    instructors = row.find_all('td')[2].text
                    instructor_list = instructors.split(';')
                ## If the evaluation page is blank in the instrucotr section
                if len(instructor_list) == 1 and instructor_list[0].strip() == '':
                    instructors = row.find_all('td')[2].text
                    instructor_list = instructors.split(';')
                    print('Blank instructor: Instructor {} Department {} Year {}'\
                          .format(instructors, dept, year))
                    ## if all of the instructor slots are blank then fill in
                    ## Unknown Instructor
                    if len(instructors.strip()) == 0:
                        instructors = "Unknown Instructor"
                        instructor_list = instructors.split(';')
                for instructor in instructor_list:
                    if ',' in instructor:
                        name_list = instructor.split(',')
                        name_list = [i.strip().lower() for i in name_list]
                    else:
                        name_list = instructor.split()
                        name_list = [i.lower() for i in name_list]
                        name_list = [name_list[0], ' '.join(name_list[1:])]
#                    name_tup = tuple([i.strip().lower() for i in name_list])
                    name = ', '.join(name_list)
                    name_tup = (name, dept)
                    instructor_num_set.add(name_tup)
#                print("find instructor", time.time() - start)
        print("At the {}th department {}, year{}".format(i, dept, year))
    instructor_num_list = sorted(list(instructor_num_set))
    count = 0
    for instruct_tup in instructor_num_list:
        count += 1
        name, dept = instruct_tup
        instructor_list = instructor_num_dict.get(name, [])
        instructor_list.append((count, dept))
        instructor_num_dict[name] = instructor_list
    return instructor_num_dict


def create_main_table(eval_url, cookie, dept_list, year_list, course_num_dict,\
                      instructor_num_dict, overwrite = True):
    course_table_dict = {} 
    instructor_table_dict = {}
    link_table_list = []
    err_count = 0
    for i, dept in enumerate(dept_list):
        for year in year_list:
            print(dept, year)
#            print("At the {}th department {}, year{}".format(i, dept, year))
            search_terms = {'Department': dept, 'AcademicYear': year,\
                            'EvalSearchType':'option-dept-search'}
#            time.sleep(0.1)
            cur_req, cur_page = get_request(eval_url, cookie, search_terms)
            table = cur_page.find('tbody')
            if table == None:
                continue
            rows = table.find_all('tr')
            for row in rows:
                link_table_class_list = []
                course_list = row.find_all('td')
                ## construct course table
                course_num = course_list[0].text
                course_title = course_list[1].text.strip()
                course_num = ' '.join(course_num.split()[0:2])
                class_section = course_num.split()[-1].strip()
                course_id = course_num_dict[course_num]
                if course_num not in course_table_dict:
                    course_table_dict[course_num] = [course_num, course_id, \
                                     course_title, dept]
                
                ## construct instructor table
                instructor_list = course_list[2].text.split(';')
                for name in instructor_list:
#                    name is blank
                    name_list = name.strip().lower().split()
                    if name_list == []:
                        continue
                    last_name = name_list[0]
                    first_name = ' '.join(name_list[1:])
                    full_name = ', '.join([last_name, first_name])
                    if full_name in instructor_num_dict:
                        if full_name not in instructor_table_dict:
                            for tup in instructor_num_dict[full_name]:
                                if dept == tup[1]:
                                    instructor_id = tup[0]
                            instructor_table_dict[full_name] = [last_name, \
                                                 first_name, instructor_id,dept]
                            link_table_class_list.append([instructor_id])
                    else:
                        last_name = name_list[-1]
                        first_name = ' '.join(name_list[:-1])
                        full_name = ', '.join([last_name, first_name])
                        if full_name in instructor_num_dict:
                            if full_name not in instructor_table_dict:
                                for tup in instructor_num_dict[full_name]:
                                    if dept == tup[1]:
                                        instructor_id = tup[0]
                                instructor_table_dict[full_name] = [last_name, \
                                                     first_name, instructor_id,dept]
                                link_table_class_list.append([instructor_id])
                        else:
                            name_found = False
                            sub_name_found = False
                            new_url = eval_url + row.find('a')['href']
                            new_req, new_page = get_request(new_url, cookie)
                            ## blank page, then ignore and continue
                            if new_page.find('p') == None:
                                continue
                            ## evluation not found, then continue
                            elif len(new_page.find('p').contents) <= 1:
                                continue
                            class_instructors = str(new_page.find('p').contents[2])
                            class_instructor_list = class_instructors.split(';')
                            for instructor in class_instructor_list:
                                instructor_sublist = []
                                for i in instructor.split(','):
                                    instructor_sublist += [j.strip().lower() for j in i.split()]
                                instructor_subset = set(instructor_sublist)
                                name_subset = set(name_list)
                                if (instructor_subset.issubset(name_subset)\
                                    or name_subset.issubset(instructor_subset))\
                                    and len(instructor_subset) != 0:
                                        name_found = True
                                        break
                                elif len(instructor_subset) != 0 \
                                        and len(name_subset) != 0:
                                    if name_list[0][0].lower() == instructor.lower().split()[0][0]\
                                            and name_list[1][0].lower() == instructor.lower().split()[1][0]:
                                        sub_name_found = True
                                        sub_instructor = instructor
                                    elif name_list[1][0].lower() == instructor.lower().split()[0][0]\
                                            and name_list[0][0].lower() == instructor.lower().split()[1][0]:
                                        sub_name_found = True
                                        sub_instructor = instructor
                            if name_found == False and sub_name_found == True:
                                print('Non-English Character met: instrcutor: {}'\
                                      .format(sub_instructor))
                                instructor = sub_instructor
                                name_found = True
                                    
                            if name_found == True:
                                instructor_name_list = instructor.split(',')
                                instructor_name_list = [i.strip().lower() \
                                        for i in instructor_name_list]
#                                print(instructor_name_list)
                                last_name = instructor_name_list[0]
                                first_name = instructor_name_list[1]
                                full_name = (', ').join(instructor_name_list)
                                for tup in instructor_num_dict[full_name]:
                                    if dept == tup[1]:
                                        instructor_id = tup[0]
                                instructor_table_dict[full_name] = [last_name, \
                                                     first_name, instructor_id, dept]
                                link_table_class_list.append([instructor_id])
                            else:
                                print('Name not found: {}, Department:{}'\
                                      .format(name, dept))
                
                ## construct the link table
                if link_table_class_list != []:
                    for entry in link_table_class_list:
                        entry.extend([course_id, year, class_section])
                        link_table_list.append(entry)
    # write course table
    if overwrite:
        outputfile = open('course_table.csv', "w", newline = "")
        outputwriter = csv.writer(outputfile)
        for course_list in list(course_table_dict.values()):
            outputwriter.writerow(["|".join([str(i) for i in course_list])])
        outputfile.close()
        # write instructor table
        outputfile = open('instructor_table.csv', "w", newline = "")
        outputwriter = csv.writer(outputfile)
        for instructor_list in list(instructor_table_dict.values()):
            outputwriter.writerow(["|".join([str(i) for i in instructor_list])])
        outputfile.close()
        # write link table
        outputfile = open('link_table.csv', "w", newline = "")
        outputwriter = csv.writer(outputfile)
        for link_list in link_table_list:
            outputwriter.writerow(["|".join([str(i) for i in link_list])])
        outputfile.close()
    return course_table_dict, instructor_table_dict, link_table_list   
                                    
                
                
            
    


if __name__ == '__main__':
    course_compile = False
    instructor_compile = False
    eval_url = 'https://evaluations.uchicago.edu/'
    # create a new Firefox session
    driver = webdriver.Firefox()
    #driver.implicitly_wait(30)
    driver.maximize_window()
    driver.get(eval_url)
    
    cookie = log_in(driver, eval_url)
    # navigate to the application home page
    driver.get("https://evaluations.uchicago.edu")
    dept_list, year_list = find_dept_year_list(eval_url, cookie)
#    dept_list = ['ECON']
#    dept_list = ['ARTV']
#    year_list = ['2015']
#    year_list = ['2010']
    dept_list_sub = []
    course_num_dict = {}
    if course_compile:
        course_num_dict = compile_course_num(eval_url, cookie, dept_list, year_list)
        with open('course_num.json', 'w') as f:
            json.dump(course_num_dict, f, ensure_ascii = False)
    if instructor_compile:
        instructor_num_dict = compile_instructor_num(eval_url, cookie, dept_list, year_list)
        with open('instructor_num.json', 'w') as f:
            json.dump(instructor_num_dict, f, ensure_ascii = False)
    with open('course_num.json') as f:
        course_num_dict = json.load(f)
    with open('instructor_num.json') as f:
        instructor_num_dict = json.load(f)
    a, b, c = create_main_table(eval_url, cookie, dept_list, year_list, course_num_dict,\
                      instructor_num_dict)
        

#driver.quit()