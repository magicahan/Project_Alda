from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.template import loader
from django.views import generic
from django import forms
import django_tables2 as tables
import traceback
import sys
import os
from django.db.models import Q

from .models import Course, Chooseins, Testinstructor
from .find_courses import find_courses
from .enroll_crawler import *
from .decision import *
from .builder import *

class CourseSearch(forms.Form):
    course1 = forms.CharField(label = 'Desired Course 1', max_length = 15, help_text = 'e.g. CMSC12300')
    course2 = forms.CharField(label = 'Desired Course 2', max_length = 15, help_text = 'e.g. MATH20300')
    course3 = forms.CharField(label = 'Desired Course 3', max_length = 15, help_text = 'e.g. ECON20000')


class EmailAdd(forms.Form):
    emailadd = forms.CharField(
        label = 'Please type in your uchicago.edu email address to get email address', 
        max_length = 100, help_text = 'e.g. nyxu@uchicago.edu',
        initial = 'xxx@uchicago.edu')

def index(request):
    context = {}
    res = None
    selectedcourses = []
    context['form2'] = None
    context['form3'] = None
    if request.method == 'POST' and 'searchbtn' in request.POST:
        form1 = CourseSearch(request.POST)
        context['form1'] = form1
        if form1.is_valid():
            course1 = form1.cleaned_data['course1']
            course2 = form1.cleaned_data['course2']
            course3 = form1.cleaned_data['course3']
            coursels = [course1, course2, course3]

            try:
                res = Course.objects.filter(coursenumber__in=coursels)
            except Exception as e:
                print('Exception caught')
                bt = traceback.format_exception(*sys.exc_info()[:3])
                context['err'] = """
                An exception was thrown in find_courses:
                <pre>{}
                {}</pre>
                """.format(e, '\n'.join(bt))
                res = None
    elif request.method == 'POST' and "schedulebtn" in request.POST:
        for i in range(1, 21):
            if 'course' + str(i) in request.POST:
                selectedcourses.append(request.POST.get('course' + str(i)))
        # context['form2'] = Course.objects.filter(cid__in=selectedcourses)
        context['form1'] = None
        dpinput = Course.objects.filter(cid__in=selectedcourses)
        coursels = []
        for input in dpinput:
            coursenum = input.coursenumber
            coursename = input.name
            courseloc = input.location
            coursetime = input.daytime
            inputls = [coursenum, coursename, courseloc, coursetime]
            coursels.append(inputls)
        dpoutput = create_schedules(coursels)
        context['form3'] = None
        if dpoutput > 0:
            context['form2'] = "Your course schedules have already been downloaded into folder."
        else:
            context['form2'] = "There's conflict in your course selection. We couldn't generate schedule."
    elif request.method == 'POST' and "emailbtn" in request.POST:
        for i in range(1, 21):
            if 'course' + str(i) in request.POST:
                selectedcourses.append(request.POST.get('course' + str(i)))
        if len(selectedcourses) != 1:
            context['form2'] = "Please only choose one course at a time to get notification."
        else:
            form3 = request.POST.get('emailadd')
            context['form3'] = form3
            emailadd = form3
            enrollinput = Course.objects.filter(cid__in=selectedcourses)[0]
            course = enrollinput.coursenumber
            coursedept = course[:4]
            coursenum = course[4:]
            enrollcrawler = main(coursedept, coursenum, emailadd)
            if enrollcrawler:
                context['form2'] = "This course is open, check your email box!"
            else:
                context['form2'] = "This course is currently closed. We'll let you know when it's open!"
            
    else:
        form1 = CourseSearch()
        context['form1'] = form1

    if res is None:
        context['result'] = None
    else:
        context['result'] = res
        context['form3'] = EmailAdd()
    
    return render(request, 'courses/index.html', context)


class CourseView(generic.DetailView):
    model = Course
    template_name = 'courses/detail.html'


class ChooseinsView(generic.DetailView):
    context = {}
    model = Chooseins
    template_name = 'courses/chooseins.html'
    context['err'] = None
    context['result'] = None
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            if len(request.POST) > 3:
                self.context['err'] = "Please choose one instructor only."
            else:
                self.context['err'] = None
                for i in range(1, 6):
                    if 'chooseins.ins'+str(i) in request.POST:
                        res = request.POST.get('chooseins.ins' + str(i))
                        namels = res.split()
                        fname = namels[0].lower()
                        lname = namels[-1].lower()
                        res = Testinstructor.objects.filter(Q(fname__contains=fname) & Q(lname__contains=lname))
                        if len(res) == 0:
                            self.context['message'] = "Sorry, this instructor doesn't have evaluation yet."
                            self.context['result'] = ['']
                        else:
                            self.context['message'] = None
                            self.context['result'] = res
        return render(request, self.template_name, self.context)
