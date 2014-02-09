from scraping import *
from events.models import *



def main(dy, mn, yr, ai, save=True):
    '''
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
    save: bool
        Saves to database if True (default)
        Only works form django shell
    
    Returns
    -------
    list_of_events: list
        List of dictionaries with all the valuable information
        title, attending, start, end, address, post, price, line_up
    '''
    events = get_events(dy, mn, yr, ai, v='day')
    list_of_events = []
    for event in events:
        html = get_html(event)
        attr = find_attributes(html)
        dc = clean_attributes(attr)
        if save:
            save_to_db(dc)
        list_of_events += [dc]
    return list_of_events


def save_to_db(dc):
    '''
    Saves the info in the database
    
    Parameters
    ----------
    dc: dict
        A dictionary containing all the valuable information
        generated with clean_attributes() function
    '''
    
    #saving location data
    location = Location()
    location.setAddress(dc['address'],  dc['post'], dc['venue'])
    location.setCoordinates()
    location.save()
    
    #saving artists data
    for performer in dc['line_up']:
        artist = Artist()
        artist.get_sc_id(performer)
        artist.save()
    
    #saving event data
    event = Event()
    event.setAttr(dc['title'], dc['start'], dc['end'], dc['price'], 
                  dc['line_up'])
    event.save()
    

    
