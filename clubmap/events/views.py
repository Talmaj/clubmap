from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response, RequestContext
from django.template.response import SimpleTemplateResponse
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
import datetime
from events.models import Event, Location, Artist

def set_times(event_list):
    '''
    Formates time
    '''
    for event in event_list:
        event.start = event.event_date_start.strftime('%H:%M') 
        event.end = event.event_date_end.strftime('%H:%M')
    return event_list

def index(request):
    context = RequestContext(request)
    event_list = Event.objects.order_by('event_date_start');
    event_list = set_times(event_list) 
    context_dic = {'events':event_list}
    return render_to_response('events/event_list.html', context_dic, context)

class EventDetailView(DetailView):
    model = Event
    template_name = "events/event_detail.html"

    def get_context_data(self,**kwargs):
        '''return today's parties'''
        context = super(EventDetailView, self).get_context_data(**kwargs)
        return context

class LocationDetailView(DetailView):
    model = Location
    template_name = "events/location_detail.html"

    def get_context_data(self,**kwargs):
        '''return today's parties'''
        context = super(LocationDetailView, self).get_context_data(**kwargs)
        return context

class ArtistDetailView(DetailView):
    model = Artist
    template_name = "events/artist_detail.html"

    def get_context_data(self,**kwargs):
        '''return today's parties'''
        context = super(ArtistDetailView, self).get_context_data(**kwargs)
        return context
