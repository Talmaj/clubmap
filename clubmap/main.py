from scraping import *
from events.models import *


def main(dy, mn, yr, ai=34, save=True):
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
    dc = get_dc(dy, mn, yr, ai)
    if save:
        save_to_db(dc)

def main_terminal(dy, mn, yr, ai=34, save=True):
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
    dc = get_dc(dy, mn, yr, ai)
    print_dc(dc)
    save = raw_input("Do you wish to save to django db? type y for yes anything else for no \n")
    if (save == "y"):
        print "saving...."
        save_to_db(dc)
    

def save_to_db(container):
    '''
    Saves the info in the database
    
    Parameters
    ----------
    dc: dict
        A dictionary containing all the valuable information
        generated with clean_attributes() function
    '''
    print container
    for dc in container:
        #TODO check if already exists
        #saving location data
        location = Location(street=dc['address'], postal_code=dc['post'], 
                            city=dc['city'], location_name=dc['venue'])
        location.setCoordinates()
        location.postal_code = 0 if location.postal_code == '' else location.postal_code
        location.save()
        
        #saving event data
        event = Event(event_name=dc['title'], event_date_start=dc['start'], 
                        event_date_end=dc['end'], price=dc['price'], 
                        location=location)
        event.save()
        
        #TODO check if already exists
        #saving artists data
        for performer in dc['line_up']:
            artist = Artist(name=performer, ignore_sc=0)
            artist.get_sc_id()
            artist.save()
            event.artists.add(artist)

    
    
