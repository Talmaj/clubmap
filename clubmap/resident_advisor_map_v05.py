import urllib2
import re
from Queue import Queue
import threading
import time
from collections import OrderedDict
from call_map import call_map
import json
from events.models import Artist, Event, Location

db = {}

start_html = '''<!DOCTYPE html>
<html><head>
  <head>
    <title>Berlin</title>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="windows-1252">
    
    <style>
      html, body, #map-canvas {
        margin: 20px;
        padding: 5px;
        height: 500px;
      }
      table {
        margin-bottom: 20px
      }
    </style>

<link rel="stylesheet" type="text/css" href="mystyle.css">
<script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false"></script>
<script src="clubs.js"></script>
<script src="variables.js"></script>
<script src="map_follow.js"></script>
<script src="mapStyle.js"></script>
</head><body><table><tr><td width=40%>'''

#end_html = 

def window_html(title, genre, venue, adress, time, price, dest_url):
    html = '''<h1 class='title'>%s</h1>
<h2 class='title2'>%s</h2>
<h1 class='venue'>%s</h1>
<h2 class='address'>%s</h2>
<p class='time'>%s</p>
<p class='price'>%s</p>
<a href="%s" class='link'>%s</a>
'''%(title, genre, venue, adress, time, price, dest_url, dest_url.split('/')[2])
    return html

# finds event urls
def get_events(dy, mn, yr, ai, v):
    url = "http://www.residentadvisor.net/events.aspx?ai=%s&v=%s&mn=%s&yr=%s&dy=%s"% \
          (ai, v, mn, yr, dy)
    f = urllib2.urlopen(url)
    events = re.findall('<a href="/event.aspx\?(.*?)">', f.read())
    return events

# finds paragraph where are all the data we need
def get_html(all_html):
    seq = '<td width="784" class=pb4>(.*?)</table></td>'
    
    paragraph = re.search(seq, all_html, re.DOTALL)
    return paragraph.group(1)

# extract the paragraph and get the data
def get_info(html, url):
    info = {}
    seq = '<div style="font-size:28px;" class="pt1 b white">(.*?)</div>'
    info['Title'] = re.search(seq, html).group(1).decode('utf-8').encode('windows-1252').split(' at ')[0]

    seq = '<td class="pb4 pr8 white">(.*?)</td>'   
    keys = ['Date', 'Time', 'Venue', 'Cost']
    values = re.findall(seq, html)
    
    for key, value in zip(keys, values):
        value = re.sub('(<.*?>)', '', value)
        value = value.decode('utf-8').encode('windows-1252')
        info[key] = value
        
        if key == 'Cost':
            info['Cost-list'] = [int(i) for i in re.findall(('(\d+)'), value)] # finds list of prices and turns them into integers
            if not info['Cost-list']: # if list is empty
                if 'free' in value.lower(): 
                    info['Cost-list'] = [0]
                elif 'tba' in value.lower():
                    info['Cost-list'] = [10] # expected value, needs adjusting
                else:
                    info['Cost-list'] = [404] # error samples
                    
    venue = '/'.join(info['Venue'].split('/')[:-1])
    address = info['Venue'].split('/')[-1].strip().replace(';', ',')
    info['club'] = venue
    info['address'] = address
    
    info['url'] = url
    #info['contentString'] = window_html(info['Title'], '', venue, address,
    #                                    info['Time'], info['Cost'], info['url'])
      
    return info

# added 15.11.2013
def get_dj_list(html):
    regex = '<div class="grey pb1">Line-up /</div><span class=black>(.*?)</span>'
    lineup = re.findall(regex, html, re.DOTALL)
    if lineup:
        cleaning = re.split('<br>', lineup[0])
        cleaning = [re.sub('<.+?>', '', dj) for dj in cleaning]
        cleaning = [re.sub('.+?:', '', dj) for dj in cleaning]
        dj_list = [re.sub('\[.*?\]|\(.*?\)|live|[\*]', '', dj).strip() for dj in cleaning]
        while '' in dj_list: dj_list.remove('')
        dj_list = [dj.strip() for dj in ','.join(dj_list).split(',')]
        dj_list = [dj.strip() for dj in '&'.join(dj_list).split('&')]
    else:
        dj_list = []
        
    return dj_list

# designs the html output
def design_html(info, url):
    html = '''<table><tr><td colspan=3> <h1 class='title'><a href="%s">%s</a></h1> </td></tr>
                    <tr> <td>%s</td> <td colspan=2> <h1 class='venue'>%s</h1> </td> </tr>
                    <tr> <td>%s</td> <td colspan=2> <p class='address'>%s</p> </td> </tr>
                    <tr> <td>%s</td> <td colspan=2> <p class='time'>%s</p> </td> </tr>
                    <tr> <td>%s</td> <td colspan=2> <p class='price'>%s</p> </td> </tr></table>\r\n'''%(info['url'], info['Title'],
                                                                         'Venue', info['club'],
                                                                         'Date', info['Date'],
                                                                         'Time', info['Time'],
                                                                         'Cost', info['Cost'])
    return html
    

# runs in threads, saves events in db and writes .html file
def process(event, q):   
    url = "http://www.residentadvisor.net/event.aspx?" + event
    f = urllib2.urlopen(url)
    temp = get_html(f.read())
    f.close()
    temp = get_info(temp)
    temp['url'] = url

    global db
    venue = temp['Venue'].split('/')[0]
    db[venue] = temp
    
    temp = design_html(temp, url)

    q.put(temp)
    html = open("clubs.html", "a")
    html.write(q.get())
    html.close()

def process_2(event):
    url = "http://www.residentadvisor.net/event.aspx?" + event
    f = urllib2.urlopen(url)
    html = f.read() 
    temp = get_html(html)
    f.close()
    temp = get_info(temp, url)
    temp['djs'] = get_dj_list(html)
    #temp['url'] = url

    global db
    #venue = temp['Venue'].split('/')[0]
    #temp['club'] = venue
    venue = temp['club']
    db[venue] = temp
    
    #temp = design_html(temp, url)
    #return temp


# main function    
def check(dy, mn, yr, n, crawl=True):
    html = open("clubs.html", "wb")
    html.write(start_html)

    if crawl:
        ai = 34#13 #London#"34" #Berlin
        v = "day"
        dy, mn, yr = str(dy), str(mn), str(yr)
        events = get_events(dy, mn, yr, ai, v)

    ##    q = Queue()
    ##    for event in events:
    ##        temp = threading.Thread(target = process, args = (event, q))
    ##        temp.start()
        
        for event in events[:n]:
            #html.write(process_2(event))
            process_2(event)

    global db
    db = OrderedDict(sorted(db.items(), key=lambda t: t[1]['Cost-list'][0]))    
    
    '''
    for d in db.values():
        html.write('<div class=events>' + d['contentString'] + '</div>')
        #html.write(d['contentString'])   
        #html.write('</p>')
        #html.write(design_html(d, 'empty'))
    
        
    #html.write(q.get())
    html.write('</td><td width="700px" height="500px" valign="top"><div id="map-canvas"></div></body></html></td></tr></table>')
    html.write("</body></html>")
    html.close()

    #call_map(db) # writes map to clubs.js
    '''
    
def main(dy, mn, yr, price):
    check(dy, mn, yr, price)

    javascript = open("clubs.js", "wb")
    for venue, info in db.items():
        javascript.write('var %s = %s' % (venue, info.decode('windows-1252')))
    javascript.close()

###########################################################################
# under construction
def sort_db(db, MAX, MIN = 0):
    temp = []
    for event in db.values():
        if max(event['Cost-list']) <= MAX and max(event['Cost-list']) >= MIN:
            temp.append(event)
    return temp

def write_from_db(List):
    html = open("clubs-sort.html", "wb")
    html.write("<html><body>")
    for event in List:
        temp = design_html(event, event['url'])
        html.write(temp)
    html.write("</body></html>")
    html.close()
###########################################################################

def write_to_variables(db):
    js = open('variables.js', 'wb')
    i = 1
    for venue, info in db.items():
        js.write('var event_%d = %s;\r\n' % (i, info))
        i += 1

    names = ['event_%d'%x for x in range(1,i)]    
    js.write('var events = [%s];\r\n' % (', '.join(names)))
    js.close()

#l = events(29,8,2013,5)

tic = time.clock()
check(14,01,2014,None)
write_to_variables(db)
#call_map(db) # writes map to clubs.js

with open('database.json', 'w') as f:
    json.dump(db, f, encoding='windows-1252')
    
toc = time.clock()
print toc-tic

for event in db.values():
    #Create Artists
    for ArtistName in event['djs']:
        #Check if exists
        if not Artist.objects.filter(name=ArtistName).exists():
            artist = Artist(name = ArtistName)
            artist.get_sc_id()
            artist.save()
    
    #Create Location
    #TODO check if exists
    if not Location.objects.filter(location_name=event['club']).exists():
        locationModel = Location()
        locationModel.location_name(event['club'])
        address = event['address'].split(',')
        street = address[0]
        postal = address[2].split(' ')[0]
        city = address[2].split(' ')[1]
        locationModel.street(street)
        locationModel.postal_code(postal)
        locationMode.city(city)
        locationModel.setCoordinates()
        locationModel.save()
    
    if not Event.objects.filter(event_name=event['Title']).exists():
        eventModel = Event()
        Event.name(event['Title'])
        
        #Get time objects
        days = event['Date'].split('-')
        times = event['Time'].split('-')
        if (len(days)==1):
            start = days[0]+ ' '+times[0]
            end = days[0]+ ' '+times[1]
        else:
            year = days[1].split(',')[2].split(' ')[2]
            start = days[0]+', '+year+ ' '+times[0]
            end = days[1]+ ', '+year+ ' '+times[1]
        start = time.strptime(start, '%A, %d %B, %Y $H:%M')
        end = time.strptime(end, '%A, %d %B, %Y $H:%M')
#write_from_db(sort_db(db,5))