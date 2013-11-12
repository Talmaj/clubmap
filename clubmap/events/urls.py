from django.conf.urls import patterns, url

from events import views

urlpatterns = patterns('',
    #calls index View /events/ will list all events for today
    url(r'^$', views.IndexView.as_view(), name='index'),
                       
                       
                       )