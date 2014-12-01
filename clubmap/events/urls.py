from django.conf.urls import patterns, url

from events import views

urlpatterns = patterns('',
    #calls index View /events/ will list all events for today
    url(r'^$', views.index),
    url(r'^event/(?P<pk>\d+)/$', views.EventDetailView.as_view(), name="detailEvent"),
    url(r'^artist/(?P<pk>\d+)/$', views.ArtistDetailView.as_view(), name="detailArtist"),
    url(r'^location/(?P<pk>\d+)/$', views.LocationDetailView.as_view(), name="detailLocation"),
)