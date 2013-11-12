from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
import datetime
from events.models import Event


class IndexView(generic.ListView):
    #model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'latest_event_list'
    
    def get_queryset(self):
        '''return today's parties'''
        return Event.objects.all()# filter(event_date = datetime.date.today())
    