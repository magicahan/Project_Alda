from django import forms

class CourseSearch(forms.Form):
	course1 = forms.CharField(label = 'Desired Course 1', max_length = 15)
	course2 = forms.CharField(label = 'Desired Course 2', max_length = 15)
	course3 = forms.CharField(label = 'Desired Course 3', max_length = 15)