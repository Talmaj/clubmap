'''
import sys
sys.path.append('/User/Alan/Documents/clubmap/clubmap')
from django.core.management import setup_environ
import clubmap.settings
setup_environ(settings)
'''
#from events.models import Artist, Event, Location
import facebook
import csv
import re
import datetime

locations = []

#EXTRACT FROM CSV
with open('facebook_links_gefunden.csv') as csvfile:
    linkreader = csv.reader(csvfile)
    linkreader.next()
    for row in linkreader:
        location_string = re.sub('[\[\]<>]','',row[1]).split(',')
        for location in location_string:
            if "/" in location:
                locations.append(location.split('/')[1].strip())
            else:
                locations.append(location.strip())

graph = facebook.GraphAPI('CAADbpT1jXBcBAM5OXAIrKt2VU52pHeIQjgoDMWQlT4ARqzwAJwJynNHfoLlKU2UfKxio7Xxxe2MLKQvROO7nnWcb2UkWBIoKteAKkubuw5Vykw6JtyZCW5xp5d3mfpNZAsNHK1M6Rmxl54IbMkaUtdIAq8bzBJjUbpteNzO1mP9cqOtC5zeUWF7iTePTdZBYoXppoiYdgZDZD')
#Crawl Facebook
for location in locations:
    try:
        location_fb = graph.get_object(location)
    except Exception, e:
        print 'error for {}'.format(location)
    #TODO: create location model save and relate id to event models
    #check if location already exists by saving fb_id
    try:
        events = graph.get_connections(location_fb['id'], 'events')
    except Exception, e:
        print 'Error retrieving events from {}'.format(location)
        
    print location_fb['name']
    for event in events['data']:
        #check if event already exists by saving also fb_id
        date = datetime.datetime.strptime('2011-03-06T03:36:45+0000','%Y-%m-%dT%H:%M:%S+0000')
        print '-----' + event['name']
        #get description
        event_detail = graph.get_object(event['id'])['description']
        #TODO: extract artists
        #TODO: create event model
        
def extractArtists(description):
    artists = []
    return artists