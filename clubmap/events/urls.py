from django.conf.urls import patterns, url

from events import views

urlpatterns = patterns('',
    #calls index View /events/ will list all events for today
    url(r'^$', views.index),
    url(r'^event/(?P<pk>\d+)/$', views.EventDetailView.as_view()),
    #url(r'^location/(?P<pk>\d+)/$', views.LocationDetailView.as_view(), name='location_detail'),
    #url(r'^event/ajax/(?P<pk>\d+)/$', views.EventAjaxDetailView.as_view(), name='event_ajax_detail'),
    #url(r'^event/ajax/(?P<pk>\d+)/$', views.LocationAjaxDetailView.as_view(), name='location_ajax_detail'),
    #url(r'^artist/ajax/(?P<pk>\d+)/$', views.ArtistScView.as_view(), name='artist_sc_detail'),
                       
                       )