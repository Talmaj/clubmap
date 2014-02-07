import re
import urllib2
import time
import requests
from time import strptime


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
    regex = '<li class="but circle-left bbox"><.+?>Listings(.+?)Upcoming events'
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
    dc['title'] = _clean_title(attr[0])
    dc['attending'] = int(attr[1])
    dc['start'], dc['end'] = _get_times(attr[2])
    dc['address'], dc['post'] = _get_address(attr[3])
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
    start: tine.struct_time
        Start time
    end: tine.struct_time
        End time
    '''

    days = re.findall('<a href="events.aspx\?(.+?)>', date)
    hours = re.findall('(\d+?:\d+?) - (\d+?:\d+)', date)[0]
    st_h, end_h = hours
    start = days[0] + '<>' + st_h
    
    if len(days) > 1:
        end = days[1] + '<>' + end_h
    else:
        end = days[0] + '<>' + end_h
    
    start = strptime(start, 'ai=34&v=day&mn=%m&yr=%Y&dy=%d"<>%H:%M')
    end = strptime(end, 'ai=34&v=day&mn=%m&yr=%Y&dy=%d"<>%H:%M')
    
    # TODO if end is before start, could do with datetime
    #if end < start:
    #    import datetime
    #    delta = datetime.timedelta(days=1)
    #    end = datetime.date(end.tm_year, end.tm_mon, end.tm_mday) + delta
    
    return start, end

def _clean_title(title):
    return re.sub(' at.*', '', title)

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
    
    return street, post

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
    line_up = line_up.split('\r\n')
    line_up = [x.replace('(live)', '').strip() for x in line_up
               if x not in ['', '-']]
    
    if labels:
        # TODO for labels
        #[_get_label(x) for x in line_up]
        pass
    else:
        line_up = [re.sub('\(.+\)', '', x) for x in line_up]
        
        # final cleaning
        line_up = [x.strip() for x in line_up if x not in ['', '-']]
    
    return line_up
