from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response, RequestContext
from django.template.response import SimpleTemplateResponse
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
import datetime
import json
from events.models import Event, Location, Artist

def set_times(event_list):
    '''
    Formates time
    '''
    for event in event_list:
        event.start = event.event_date_start.strftime('%H:%M') 
        event.end = event.event_date_end.strftime('%H:%M')
    return event_list
'''
index page is configured to show a today event view. Context data is obsolet as we fetch data over javascript.
'''
def index(request):
    context = RequestContext(request)
    event_list = Event.objects.order_by('event_date_start');
    event_list = set_times(event_list) 
    context_dic = {'events':event_list}
    return render_to_response('events/mapDay.html', context_dic, context)

'''
Kind of a dummy view to access map directly over url
not sure if any context data will be needed as all data will be fetched from javascript using ajax
'''
def mapView(request,day=0,month=0,year=0):
    context = RequestContext(request)
    event_list = Event.objects.order_by('event_date_start');
    event_list = set_times(event_list) 
    context_dic = {'events':event_list}
    return render_to_response('events/map_view.html', context_dic, context)

'''
Returns a JSON data object containing all events with their artists locations and corresponding markers
SoundMap.js accesses this to build the map and player UI

TODO make sensitive to entered date. For testing purposes all event in db are returned.
'''
def ajaxView(request,day=0,month=0,year=0):
    event_list = Event.objects.today().order_by('event_date_start');
    data = [event.as_dic() for event in event_list]
    return HttpResponse(json.dumps({"data":data}), content_type="application/json")

'''
Generates necessary HTML to render a single event
'''
class EventDetailView(DetailView):
    model = Event
    template_name = "events/event_detail.html"

    def get_context_data(self,**kwargs):
        '''return today's parties'''
        context = super(EventDetailView, self).get_context_data(**kwargs)
        return context

'''
Generates necessary HTML to render a single Location
'''
class LocationDetailView(DetailView):
    model = Location
    template_name = "events/location_detail.html"

    def get_context_data(self,**kwargs):
        '''return today's parties'''
        context = super(LocationDetailView, self).get_context_data(**kwargs)
        return context

'''
Generates necessary HTML to render a single artist
shoud we support this? Artists are not really a focus on ourplattform so far
But they should care about their profile in the future
'''
class ArtistDetailView(DetailView):
    model = Artist
    template_name = "events/artist_detail.html"

    def get_context_data(self,**kwargs):
        '''return today's parties'''
        context = super(ArtistDetailView, self).get_context_data(**kwargs)
        return context
