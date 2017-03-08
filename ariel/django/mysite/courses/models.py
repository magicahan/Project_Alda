import datetime
from django.db import models
from django.utils import timezone
#from django.utils.encoding import python_2_unicode_compatible

class Course(models.Model):
	coursenumber = models.CharField(max_length = 15)
	career = models.CharField(max_length = 30)
	condition = models.CharField(max_length = 10)
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
		return str(self.coursenumber)

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
    	return self.question_text

    def was_published_recently(self):
    	now = timezone.now()
    	return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
    	return self.choice_text
