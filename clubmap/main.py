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
        location.published = True
        location.postal_code = 0 if location.postal_code == '' else location.postal_code
        if(Location.objects.filter(location_name=dc['venue'], street=dc['address']).exists()):
            print "location already exists"
            #might work as long we stay in one city
            location = Location.objects.get(location_name=dc['venue'], street=dc['address'])
        else:
            location.save()
        
        #saving event data
        event = Event(event_name=dc['title'], event_date_start=dc['start'], 
                        event_date_end=dc['end'], price=dc['price'], 
                        location=location)
        event.published = True
        event.gay = False

        if(Event.objects.filter(event_date_start=dc['start'], event_name = dc['title']).exists()):
            print "event already exists in db";
            event = Event.objects.get(event_date_start=dc['start'], event_name = dc['title']);
        else:
            event.save()
        
        #TODO check if already exists
        #saving artists data
        for performer in dc['line_up']:
            artist = Artist(name=performer, ignore_sc=False)
            artist.get_sc_id()
            if (artist.soundcloud_id != None):
                if (Artist.objects.filter(soundcloud_id=artist.soundcloud_id).exists()):
                    #artist already exists so to link the event we use the existing one
                    artist = Artist.objects.get(soundcloud_id = artist.soundcloud_id)
                else:
                    #sc id is not in database add artist
                    artist.save()
            else:
                #we don't have a sc_id check by name
                if(Artist.objects.filter(name = artist.name).exists()):
                    artist = Artist.objects.get(soundcloud_id = artist.soundcloud_id)
                else:
                    artist.save()
            
            event.artists.add(artist)
    
    
