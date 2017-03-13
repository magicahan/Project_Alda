### Project Alda
### Django Data Loading
### Ningyin Xu Mar. 4th

###############################################################################
    
    # After setting up models in django, you can use this file to load data
    # into them. 

###############################################################################

from courses.models import Course, Chooseins, Instructor, InstructorCourse
import json
import csv
import pandas as pd
import pickle

with open('course_output.json') as f:
	courses_dict = json.load(f)

coursedf = pd.DataFrame.from_dict(courses_dict, orient='index')
coursedf.sort_index(axis=1, inplace = True)
courses_dict = coursedf.T.to_dict('list')

def loaddatatoCourse(courses_dict):
	coursemodells = []
	for key, value in courses_dict.items():
		course = Course(cid = key,
		career = value[0],
		condition = value[1],
		coursenumber = value[2],
		daytime = value[3],
		description = value[4],
		instructor = value[5],
		location = value[6],
		name = value[7],
		section = value[8],
		sectionid = value[9],
		subsections = value[10],
		coursetype = value[11])
		course.save()
		coursemodells.append(course)
	return coursemodells


def loaddatatoChooseins():
	courseset = Course.objects.all()
	for i in courseset:
		ins = i.instructor
		pk = i.cid
		insls = ins.split(',')
		ins_num = len(insls)
		argls = [str() for i in range(5)]
		for n in range(1, ins_num+1):
			argls[n-1] = insls[n-1]
		test = Chooseins(
			inspk = i,
			ins1 = argls[0],
			ins2 = argls[1],
			ins3 = argls[2],
			ins4 = argls[3],
			ins5 = argls[4]
			)
		test.save()
	return None


def loadInstructor():
	with open('avg_score_ins_final', 'rb') as f:
		avgscore_dict = pickle.load(f)
	for key, value in avgscore_dict.items():
		if len(value['pos']) < 6:
			for i in range(6 - len(value['pos'])):
				value['pos'].append(str())
		if len(value['neg']) < 6:
			for i in range(6 - len(value['neg'])):
				value['neg'].append(str())
		instr = Instructor(instructor_id = value['instructor_id'],
		dept = value['dept'],
		fname=value['first_name'],
		lname = value['last_name'],
		pos1 = value['pos'][0],
		pos2 = value['pos'][1],
		pos3 = value['pos'][2],
		pos4 = value['pos'][3],
		pos5 = value['pos'][4],
		pos6 = value['pos'][5],
		neg1 = value['neg'][0],
		neg2 = value['neg'][1],
		neg3 = value['neg'][2],
		neg4 = value['neg'][3],
		neg5 = value['neg'][4],
		neg6 = value['neg'][5],
		num_response = int(float(value['num_response'])),
		avg_score = value['avg_score'])
		instr.save()
	return None


def loadInstructorCourse():
	with open('avg_score_ins_course_final', 'rb') as f:
		avgscorecourse_dict = pickle.load(f)
	for key, value in avgscorecourse_dict.items():
		if len(value['pos']) < 6:
			for i in range(6 - len(value['pos'])):
				value['pos'].append(str())
		if len(value['neg']) < 6:
			for i in range(6 - len(value['neg'])):
				value['neg'].append(str())
		if isinstance(value['num_response'], type(None)):
			value['num_response'] = 0
		if isinstance(value['first_name'], type(None)):
			value['first_name'] = ''
		if isinstance(value['last_name'], type(None)):
			value['last_name'] = ''
		if isinstance(value['avg_score'], type(None)):
			value['avg_score'] = 0
		if isinstance(value['instructor_id'], type(None)):
			value['instructor_id'] = 999999999
		instrcourse = InstructorCourse(
		icid = key,
		coursename = value['course_num'],
		coursetitle = value['course_title'],
		courseid = int(value['course_id']),
		instructor_id = value['instructor_id'],
		dept = value['dept'],
		fname = value['first_name'],
		lname = value['last_name'],
		pos1 = value['pos'][0],
		pos2 = value['pos'][1],
		pos3 = value['pos'][2],
		pos4 = value['pos'][3],
		pos5 = value['pos'][4],
		pos6 = value['pos'][5],
		neg1 = value['neg'][0],
		neg2 = value['neg'][1],
		neg3 = value['neg'][2],
		neg4 = value['neg'][3],
		neg5 = value['neg'][4],
		neg6 = value['neg'][5],
		coursenum_response = int(float(value['num_response'])),
		courseavg_score = value['avg_score'])
		instrcourse.save()
	return None

















