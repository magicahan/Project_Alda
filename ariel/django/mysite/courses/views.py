from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.template import loader
from django.views import generic
from django import forms
import django_tables2 as tables
import traceback
import sys

from .models import Course
from .find_courses import find_courses

COLUMN_NAMES = dict(
        Select='Select',
        courseid='Courseid',
        coursenumber='Course',
        name='Name',
        career='Undergrad/Grad',
        condition='Open/Closed',
        daytime='Day/Time',
        description='Course Description',
        instructor='Instructor Name(s)',
        location='Location',
        section='Section',
        sectionid='Sectionid',
        subsections='Labs/Discussions',
        coursetype='LEC/SEM',
)


class CourseSearch(forms.Form):
    course1 = forms.CharField(label = 'Desired Course 1', max_length = 15, help_text = 'e.g. CMSC12300')
    course2 = forms.CharField(label = 'Desired Course 2', max_length = 15, help_text = 'e.g. MATH20300')
    course3 = forms.CharField(label = 'Desired Course 3', max_length = 15, help_text = 'e.g. ECON20000')


class CourseSelect(forms.Form):
    Select = forms.BooleanField(label = 'Select', required = False)

def index(request):
    context = {}
    res = None
    if request.method == 'POST':
        form = CourseSearch(request.POST)
        if form.is_valid():
            #return HttpResponseRedirect('/searchresults/')
            args = {}
            course1 = form.cleaned_data['course1']
            course2 = form.cleaned_data['course2']
            course3 = form.cleaned_data['course3']
            if course1:
                args['course1'] = course1
            if course2:
                args['course2'] = course2
            if course3:
                args['course3'] = course3
            try:
                res = find_courses(args)
            except Exception as e:
                print('Exception caught')
                bt = traceback.format_exception(*sys.exc_info()[:3])
                context['err'] = """
                An exception was thrown in find_courses:
                <pre>{}
                {}</pre>
                """.format(e, '\n'.join(bt))

                res = None
    else:
        form = CourseSearch()

    if res is None:
        context['result'] = None
    elif isinstance(res, str):
        context['result'] = None
        context['err'] = res
        result = None
        cols = None

    else:
        columns, result = res

        # Wrap in tuple if result is not already
        if result and isinstance(result[0], str):
            result = [(r,) for r in result]

        # result1 = []
        # for res in result:
        #     selectchoice = CourseSelect(request.POST)
        #     res = (selectchoice,) + res
        #     result1.append(res)
        columns.insert(0, 'Select')
        # columns.insert(0, '')
        context['result'] = result
        context['num_results'] = len(result)
        context['columns'] = [COLUMN_NAMES.get(col, col) for col in columns]

    context['form'] = form
    selected = request.POST.getlist('checks')
    context['selected'] = selected

    return render(request, 'courses/index.html', context)

# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'courses/detail.html'

# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'courses/results.html'

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'courses/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('courses:results', args=(question.id,)))

# def get_courses(request):
#     if request.method == 'POST':
#         form = CourseSearch(request.POST)
#         if form.is_valid():
#             return HttpResponseRedirect('/searchresults/')
#     else:
#         form = CourseSearch()

#     return render(request, 'courses/coursesearch.html', {'form': form})
