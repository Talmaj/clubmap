#from events.models import Artist, Event, Location
import facebook
import csv
import re
import datetime
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

if(len(sys.argv) < 3):
    print bcolors.FAIL + "usage: crawlFB.py LINKSFILE API_KEY" + bcolors.ENDC
    exit()
api_key = sys.argv[2]
path = sys.argv[1]
locations = []

#EXTRACT FROM CSV
csvfile = open(path, 'rb')
linkreader = csv.reader(csvfile)
linkreader.next()
for row in linkreader:
    print(row)
    location_string = re.sub('[\[\]<>]','',row[1]).split(',')
    for location in location_string:
        if "/" in location:
            locations.append(location.split('/')[1].strip())
        else:
            locations.append(location.strip())

#Always replace with a fresh key
graph = facebook.GraphAPI(api_key)

#Crawl Facebook
for location in locations:
    try:
        location_fb = graph.get_object(location)
    #TODO: create location model save and relate id to event models
    #check if location already exists by saving fb_id
        events = graph.get_connections(location_fb['id'], 'events')
        print bcolors.OKGREEN + location_fb['name'] + bcolors.ENDC

        for event in events['data']:
            #check if event already exists by saving also fb_id
            date = datetime.datetime.strptime('2011-03-06T03:36:45+0000','%Y-%m-%dT%H:%M:%S+0000')
            print '-----' + event['name']
            #get description
            event_detail = graph.get_object(event['id'])['description']
            #TODO: extract artists
            #TODO: create event model
    except Exception, e:
        print bcolors.WARNING + 'Error retrieving events from {}'.format(location) + bcolors.ENDC
        

def cleanName(string):
    string = string.strip().strip('/').strip('/').strip()
    return string
        
def extractArtists(description):
    description = description.split('<br />')
    description = [re.sub('<.*?>', '', x) for x in description]
    regexes = ['(.*?)\(.*?\)', '(.*?)\[.*?\]']
    artists = [re.match('|'.join(regexes), x) for x in description]
    artists = [x.group(1) for x in artists if bool(x)]
    #artists = [cleanName(x) for x in artists]
    return artists

