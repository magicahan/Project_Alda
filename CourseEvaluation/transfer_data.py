#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 12:49:38 2017

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
import re
import pickle
import sqlite3
import pandas as pd

table_file  = ['course_table.csv', 'instructor_table.csv', 'link_table.csv', 
               'instructor_avgscore.csv', 'instructor_score.csv', \
               'instructor_comments.csv', 'score_combine.csv', 'score_combine_course.csv']
col_name_list = [['course_num', 'course_id', 'course_title', 'dept'],\
                 ['last_name', 'first_name','instructor_id','dept'],
                 ['instructor_id', 'course_id', 'year', 'class_section', 'quarter'],\
                 ['course_id', 'year', 'class_section', 'quarter', 'instructor_id',\
	             'avg_score', 'num_response' ],\
                  ['course_id', 'year', 'class_section','quarter','instructor_id',\
                   'score_term','avg_score', 'num_response'],\
                   ['course_id', 'year', 'class_section', 'quarter', 'instructor_id', 
	               'comments'],
                    ['dept', 'last_name', 'first_name', 'instructor_id', 'num_response',\
                     'avg_score'],
                     ['course_num', 'course_id', 'course_title', 'dept', 'last_name', 'first_name', 'instructor_id', 'num_response',\
                     'avg_score']
                   ]

def transfer_data():
    '''
    A function to transfer the csv file for a django fixure structure
    '''
    dict_data_list = []
    for i, file_name in enumerate(table_file):
        # the function for creating the files other than comment
        if i != 5:
            with open(file_name, 'rt', encoding = 'ascii', errors = 'ignore') as fb:
                db_reader = csv.reader(fb, delimiter = '|')
                db_list = [ j for j in db_reader]
            for m, entry in enumerate(db_list):
                if len(entry) != len(col_name_list[i]):
                    db_list[m] = list(entry[0].split('|'))
            data = pd.DataFrame(db_list, columns = col_name_list[i])
            data_dict = data.to_dict('index')
            dict_data_list.append(data_dict)
            data_file_name = file_name.split('.')[0]
            ## dump to a pickle file
            with open(data_file_name, 'wb') as f:
                pickle.dump(data_dict, f)
        else:
            with open(file_name, 'rt', encoding = 'ascii', errors = 'ignore') as fb:
                db_reader = csv.reader(fb, delimiter = '|')
                db_list = [ j for j in db_reader]
            # split the entries that csv reader fails to read
            for m, entry in enumerate(db_list):
                if len(entry) != 6:
                    db_list[m] = list(entry[0].split('|'))
            data = pd.DataFrame(db_list, columns = col_name_list[i])
            data_dict = data.to_dict('index')
            dict_data_list.append(data_dict)
            data_file_name = file_name.split('.')[0]
            with open(data_file_name, 'wb') as f:
                pickle.dump(data_dict, f)
    return dict_data_list

if __name__ == '__main__':
    a= transfer_data()
    with open('instructor_avgscore', 'rb') as f:
        b = pickle.load(f)
    with open('extracted_words.json', 'rt') as f:
        word_dict = json.load(f)
    with open('instructor_table', 'rb') as f:
        ins_table = pickle.load(f)
    with open('score_combine', 'rb') as f:
        score_instructor = pickle.load(f)
    with open('score_combine_course', 'rb') as f:
        score_ins_course = pickle.load(f)
    # integrate the data into two tables
    for key, value in score_instructor.copy().items():
        instructor_id = str(value['instructor_id'])
        if instructor_id in word_dict:
            word_one_dict = word_dict[instructor_id]
            value['neg'] = word_one_dict['neg']
            value['pos'] = word_one_dict['pos']
        else:
            value['neg'] = ['No Comments']
            value['pos'] = ['No Comments']
        score_instructor[key] = value
    for key, value in score_ins_course.copy().items():
        instructor_id = str(value['instructor_id'])
        if instructor_id in word_dict:
            word_one_dict = word_dict[instructor_id]
            value['neg'] = word_one_dict['neg']
            value['pos'] = word_one_dict['pos']
        else:
            value['neg'] = ['No Comments']
            value['pos'] = ['No Comments']
        score_ins_course[key] = value
    with open('avg_score_ins', 'wb') as f:
        pickle.dump(score_instructor, f)
    with open('avg_score_ins_course', 'wb') as f:
        pickle.dump(score_ins_course, f)
        
        