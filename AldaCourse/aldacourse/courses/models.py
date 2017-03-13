### Project Alda
### Django Model script
### Ningyin Xu Mar. 4th

###############################################################################
    
    # After setting up models, you can use loaddata.py from loaddata folder
    # to load data into models.

###############################################################################

import datetime
from django.db import models
from django.db.models import Q
from django.utils import timezone

class Course(models.Model):
	cid = models.CharField(max_length=30, primary_key = True)
	career = models.CharField(max_length = 30)
	condition = models.CharField(max_length = 10)
	coursenumber = models.CharField(max_length = 15)
	daytime = models.CharField(max_length = 50, blank = True)
	description = models.CharField(max_length = 5000, blank = True)
	instructor = models.CharField(max_length = 100, blank = True)
	location = models.CharField(max_length = 50, blank = True)
	name = models.CharField(max_length = 100, blank = True)
	section = models.CharField(max_length = 5, blank = True)
	sectionid = models.CharField(max_length = 10, blank = True)
	subsections = models.CharField(max_length = 5000, blank = True)
	coursetype = models.CharField(max_length = 5, blank = True)
	
	def __str__(self):
		return str(self.cid)


class Chooseins(models.Model):
	inspk = models.CharField(max_length=30, primary_key = True, default='')
	ins1 = models.CharField(max_length=30)
	ins2 = models.CharField(max_length=30, blank = True)
	ins3 = models.CharField(max_length=30, blank = True)
	ins4 = models.CharField(max_length=30, blank = True)
	ins5 = models.CharField(max_length=30, blank = True)

	def __str__(self):
		return str(self.inspk)


class Instructor(models.Model):
	instructor_id = models.IntegerField(primary_key = True)
	dept = models.CharField(max_length=30, blank = True)
	fname = models.CharField(max_length=50, blank = True, default='')
	lname = models.CharField(max_length=50, blank = True, default='')
	pos1 = models.CharField(max_length=30, blank = True, default='')
	pos2 = models.CharField(max_length=30, blank = True, default='')
	pos3 = models.CharField(max_length=30, blank = True, default='')
	pos4 = models.CharField(max_length=30, blank = True, default='')
	pos5 = models.CharField(max_length=30, blank = True, default='')
	pos6 = models.CharField(max_length=30, blank = True, default='')
	neg1 = models.CharField(max_length=30, blank = True, default='')
	neg2 = models.CharField(max_length=30, blank = True, default='')
	neg3 = models.CharField(max_length=30, blank = True, default='')
	neg4 = models.CharField(max_length=30, blank = True, default='')
	neg5 = models.CharField(max_length=30, blank = True, default='')
	neg6 = models.CharField(max_length=30, blank = True, default='')
	num_response = models.IntegerField()
	avg_score = models.FloatField()

	def __str__(self):
		return str(self.instructor_id)


class InstructorCourse(models.Model):
	icid = models.IntegerField(primary_key = True)
	dept = models.CharField(max_length=30, blank = True)
	fname = models.CharField(max_length=50, blank = True, default='')
	lname = models.CharField(max_length=50, blank = True, default='')
	pos1 = models.CharField(max_length=30, blank = True, default='')
	pos2 = models.CharField(max_length=30, blank = True, default='')
	pos3 = models.CharField(max_length=30, blank = True, default='')
	pos4 = models.CharField(max_length=30, blank = True, default='')
	pos5 = models.CharField(max_length=30, blank = True, default='')
	pos6 = models.CharField(max_length=30, blank = True, default='')
	neg1 = models.CharField(max_length=30, blank = True, default='')
	neg2 = models.CharField(max_length=30, blank = True, default='')
	neg3 = models.CharField(max_length=30, blank = True, default='')
	neg4 = models.CharField(max_length=30, blank = True, default='')
	neg5 = models.CharField(max_length=30, blank = True, default='')
	neg6 = models.CharField(max_length=30, blank = True, default='')
	coursenum_response = models.IntegerField()
	courseavg_score = models.FloatField()
	instructor_id = models.IntegerField()
	coursename = models.CharField(max_length=30, blank = True, default='')
	coursetitle = models.CharField(max_length=30, blank = True, default='')
	courseid = models.IntegerField()

	def __str__(self):
		return str(self.icid)




























