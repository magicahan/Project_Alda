from django.conf.urls import url

from . import views

app_name = 'courses'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # # ex: /polls/5/
    url(r'^(?P<pk>[A-Z]+[0-9]+[[0-9]+])/$', views.CourseView.as_view(), name='detail'),
    url(r'^chooseins/(?P<pk>[A-Z]+[0-9]+[[0-9]+])/$', views.ChooseinsView.as_view(), name='chooseins'),
    # # ex: /polls/5/results/
    # url(r'^(?P<pk>[0-9]+)$', views.InstructorView.as_view(), name='instructordetail'),
    # # ex: /polls/5/vote/
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    # url(r'^coursesearch$', views.get_courses, name = 'coursesearch'),
]