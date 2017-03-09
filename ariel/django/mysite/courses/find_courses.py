### Project Alda
### Find courses (SQL query helper function for django)
### Ningyin Xu

import sqlite3
import json
import re
import os

DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'course-info.db')

def find_courses(args_from_ui):
	if len(args_from_ui) == 0:
		return ([],[])

	else:
		db = sqlite3.connect(DATABASE_FILENAME)
		c = db.cursor()
		coursels = []
		for key, value in args_from_ui.items():
			coursels.append(value)

		query = 'SELECT coursenumber, section, name, career, condition, '+\
		'daytime, instructor, location, coursetype FROM'+\
		' courses WHERE coursenumber = ? or coursenumber = ? or coursenumber = ?'
		args = tuple(coursels)

		r = c.execute(query, args)
		resultsls = r.fetchall()
		namesls = get_header(c)
		db.close()

		return (namesls, resultsls)

def get_header(cursor):
	'''
	Given a cursor object, returns the appropriate header (column names)
	'''
	desc = cursor.description
	header = ()

	for i in desc:
		header = header + (clean_header(i[0]),)

	return list(header)

def clean_header(s):
	'''
	Removes table name from header
	'''
	for i in range(len(s)):
		if s[i] == ".":
			s = s[i+1:]
			break

	return s
