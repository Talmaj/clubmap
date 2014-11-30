from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response, RequestContext
from django.template.response import SimpleTemplateResponse
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
import datetime
from events.models import Event, Location, Artist


def index(request):
    context = RequestContext(request)
    event_list = Event.objects.order_by('event_date_start');
    context_dic = {'events':event_list}
    return render_to_response('events/event_list.html', context_dic, context)

class IndexView(ListView):
    model = Event
    template_name = 'events/event_list2.html'
    context_object_name = 'latest_event_list'
    
    def get_context_data(self,**kwargs):
        '''return today's parties'''
        context = super(IndexView, self).get_context_data(**kwargs)
        context['events'] = Event.objects.all()# filter(event_date = datetime.date.today())
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    
    def get_context_data(self, **kwargs):
        #Call super class method
        context = super(EventDetailView, self).get_context_data(**kwargs)
        context['lineup'] = Event.artists.all()
        return context
