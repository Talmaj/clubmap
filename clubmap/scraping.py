import re
import urllib2
import time
import requests
#from time import strptime
import datetime as dt


def get_events(dy, mn, yr, ai, v='day'):
    '''
    You insert date and recieve ids from events.
    
    Parameters
    ----------
    dy: str
        Day - two digits
    mn: str
        Month - two digits
    yr: str
        Year - four digits
    ai: str
        City id (Berlin 34)
    v: str
        Other parameter (week, day, etc.)
    
    Returns
    -------
    events: list
        List of Ids of events
    '''

    dy, mn, yr, ai = [str(i) for i in [dy, mn, yr, ai]]

    url = "http://www.residentadvisor.net/events.aspx?ai=%s&v=%s&mn=%s&yr=%s&dy=%s"% \
          (ai, v, mn, yr, dy)
    f = urllib2.urlopen(url)
    events = re.findall('<a href="/event.aspx\?(\d*?)">', f.read())
    return events


def get_html(event_id):
    '''
    Returns site's html string
    
    Parameters
    ----------
    event_id: str
        Id of the event
    
    Returns
    -------
    html: str
        html string
    '''
    
    # TODO problems with encoding, weird signs
    url = "http://www.residentadvisor.net/event.aspx?" + event_id
    #f = urllib2.urlopen(url)
    r = requests.get(url)
    html = r.text
    #html = f.read()
    return html


def clean_tags(text):
    text = re.sub('<.+?>', '', text)
    return text


def find_attributes(html):
    '''
    Finds all the important attributes from each event
    
    Parameters
    ----------
    html: str
        Site's html string
    
    Returns
    -------
    output: list
        List of all attributes
        output = [title, attending, date, address, price, line_up]
    '''
    
    # select only important part
    regex = '<li class="but circle-left bbox"><.+?>Listings(.+?)to join the conversation.</h2>'
    html = re.findall(regex, html, re.DOTALL)[0]
    
    regex = '<h1>(.*?)</h1>'
    title = re.findall(regex, html, re.DOTALL)[0]
    
    regex = '<h1 id="MembersFavouriteCount" class="favCount">(\d+?)</h1>'
    attending = re.findall(regex, html, re.DOTALL)[0]
    
    regex = '<li.*?><div>Date /</div>(.+?)</li>'
    date = re.findall(regex, html, re.DOTALL)[0]
    
    regex = '<li.*?><div>Venue /</div>(.+?)</li>'
    address = re.findall(regex, html, re.DOTALL)[0]
    
    regex = '<li.*?><div>Cost /</div>(.+?)</li>'
    price = re.findall(regex, html, re.DOTALL)[0]
    
    regex = '<span class="f12 grey">Line-up /</span>(.+?)</p>'
    line_up = re.findall(regex, html, re.DOTALL)[0]
    
    output = [title, attending, date, address, price, line_up]
    return output


def clean_attributes(attr):
    '''
    Prepares attributes to put them in the DataBase
    
    Parameters
    ----------
    attr: list
        List from find_attributes()
    
    Returns
    -------
    attr: list
        Preared data for the DataBase
    '''
    
    dc = {}
    dc['title'], dc['venue'] = _clean_title(attr[0])
    dc['attending'] = int(attr[1])
    dc['start'], dc['end'] = _get_times(attr[2])
    dc['address'], dc['post'], dc['city'] = _get_address(attr[3])
    dc['price'] = _money_parser(attr[4])
    dc['line_up'] =  _get_line_up(attr[5])
    
    return dc


def _get_times(date):
    '''
    Returns start and end time
    
    Parameters
    ----------
    date: str
        Date string that we fetch with find_attributes()
    
    Returns
    -------
    start: time.struct_time
        Start time
    end: time.struct_time
        End time
    '''

    days = re.findall('<a href="events.aspx\?(.+?)>', date)
    hours = re.findall('(\d+?:\d+?)', date)

    if len(hours) > 1:
        st_h, end_h = hours
    else:
        st_h = hours[0]
        end_h = ''

    start = days[0] + '<>' + st_h
    
    if len(days) > 1:
        end = days[1] + '<>' + end_h
    else:
        end = days[0] + '<>' + end_h
    
    start = dt.datetime.strptime(start, 'ai=34&v=day&mn=%m&yr=%Y&dy=%d"<>%H:%M')
    if end_h:
        end = dt.datetime.strptime(end, 'ai=34&v=day&mn=%m&yr=%Y&dy=%d"<>%H:%M')
    else:
        #TODO better solution
        end = start
    
    # TODO if end is before start, could do with datetime
    if end < start:
        delta = dt.timedelta(days=1)
        end = end + delta
    
    return start, end

def _clean_title(title):
    '''
    Parameters
    ----------
    title: str
        Title string from find_attributes()

    Returns
    -------
    party_name: str
        Name of the party
    venue: str
        Venue name
    '''
    party_name = re.sub(' at.*', '', title)
    venue = re.sub('.*at ', '', title)

    return party_name, venue

def _get_address(address):
    '''
    Returns Address and Post number
    
    Parameters
    ----------
    address: str
        Address string that we fetch with find_attributes()
    
    Returns
    -------
    street: str
        Address
    post:
        Post number
    '''
    
    address = [clean_tags(x).strip() for x in address.split('<br />')]
    venue = address[0]
    temp = address[1].split('; ')
    street = temp[0]
    post = re.findall('(\d+) ', temp[-1])[0]
    city = re.sub(post, '', temp[-1]).strip(';').strip()
    
    return street, post, city

def _money_parser(cost):
    '''
    Parses the cost string. If contains free, returns 0, else cost
    
    Parameters
    ----------
    cost: str
        Cost string that we fetch with find_attributes()
    
    Returns
    -------
    cost: int
        Cost as integer
    '''
    
    if 'free' in cost.lower():
        return 0
    else:
        costs = re.findall('\d+', cost)
    
    if len(costs) == 1:
        return int(costs[0])
    #TODO else:    
    else:
        return 9.5


# <codecell>

def _get_label(string):
    '''
    Returns tuple of Artist and Label if label exists
    
    Parameters
    ----------
    string: str
        String after usage of _get_line_up()
    
    Returns
    -------
    (artist, label): tuple
        Artist name and label, if exists else ''
    '''
    
    if '(' in string:
        artist, label = re.findall('(.+)\((.+)\)', string)[0]
    else:
        artist = string
        label = ''
    
    return (artist, label)

def _get_line_up(line_up, labels=False):
    '''
    Returns lineup list
    
    Parameters
    ----------
    line_up: str
        Line up string that we fetch with find_attributes()
    labels: bool
        If we want also labels
    
    Return
    ------
    line_up: list
        List of Artists
    '''
    
    line_up = line_up.strip('\r\n').strip()
    line_up = clean_tags(line_up)

    # if each artist in new row
    line_up = line_up.split('\r\n')
    line_up = [x.replace('(live)', '').strip() for x in line_up
               if x not in ['', '-']]
    
    # if lineup written in a single row and separated with //
    if len(line_up) == 1:
        line_up = line_up[0].split(' // ')
        if len(line_up) == 1: 
            line_up = line_up[0].split(', ')
            # TODO if a lot of this cases, can do some function
        line_up = [x.strip() for x in line_up]

    line_up = _clean_line_up(line_up)

    if labels:
        # TODO for labels
        #[_get_label(x) for x in line_up]
        pass
    else:
        # if label in brackets
        line_up = [re.sub('\(.+\)', '', x) for x in line_up]
        line_up = [re.sub('\[.+\]', '', x) for x in line_up]
        # if label after ///
        line_up = [re.sub('.*( ///*)', '', x) for x in line_up]


        # final cleaning
        line_up = [x.strip() for x in line_up if x not in ['', '-']]
    print line_up
    return line_up

def _clean_line_up(line_up):
    '''
    Cleans the line up list of all the stupid things
    # TODO it should remove the name of the club where it is playing
    # add stuff with usage, mostly .strip and .replace

    Parameters
    ----------
    line_up: list
        List of Artists, uncleaned

    Returns: list
        Cleaned line up list
    '''

    exclude = ['TBA', 'tba', '...', 'Berlin']
    line_up = [x.strip('Main:').strip('Mini:') for x in line_up 
                if x not in exclude and not x.startswith('http://')]
    return line_up

