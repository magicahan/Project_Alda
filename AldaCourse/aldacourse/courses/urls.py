from django.conf.urls import url

from . import views

app_name = 'courses'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>[A-Z]+[0-9]+[[0-9]+])/$', views.CourseView.as_view(), name='detail'),
    url(r'^chooseins/(?P<pk>[A-Z]+[0-9]+[[0-9]+])/$', views.ChooseinsView.as_view(), name='chooseins'),
]