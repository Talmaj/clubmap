from scraping import *
from events.models import *
# import pickle
import pytz
TEST_PATH = '/Users/Talmaj/Projects'

TIMEZONES = {34: pytz.timezone("Europe/Berlin")}

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
    # pickling for testing purposes, not to need to scrape all the time
    # pickle.dump(dc, open(TEST_PATH + '/all_events.pkl', 'w'))
    # dc = pickle.load(open(TEST_PATH + '/all_events.pkl', 'r'))
    if save:
        save_to_db(dc, ai)

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


def save_to_db(container, ai=34):
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
        name = ""
        try:
            #TODO check if already exists
            if Location.objects.filter(location_name=dc['venue'], street=dc['address']).exists():
                print "location already exists"
                # might work as long we stay in one city
                location = Location.objects.get(location_name=dc['venue'], street=dc['address'])
            else:
                # saving location data
                location = Location(street=dc['address'], postal_code=dc['post'],
                                    city=dc['city'], location_name=dc['venue'])
                location.setCoordinates()
                location.published = True
                location.postal_code = 0 if location.postal_code == '' else location.postal_code # funny stuff
                location.save()

            # localizing timezones & other fixes TODO move to scraping script
            #dc['start'] = TIMEZONES[ai].localize(dc['start'])
            #dc['end'] = TIMEZONES[ai].localize(dc['end'])
            dc['title'] = dc['title'].strip(u'\U0001f4e3').strip()

            # saving event data
            event = Event(event_name=dc['title'], event_date_start=dc['start'],
                            event_date_end=dc['end'], price=dc['price'],
                            location=location, ra_id=dc['ra_id'], gay=False)
            event.published = True


            if(Event.objects.filter(event_date_start=dc['start'], event_name = dc['title']).exists()):
                print "event already exists in db";
                event = Event.objects.get(event_date_start=dc['start'], event_name=dc['title']);
            else:
                event.save()

            # temp
            if dc['line_up']:
                dc['line_up'] = clean_lineup(dc['line_up'])
            # TODO check if already exists
            # saving artists data
            for performer in dc['line_up']:

                # TODO better clean the line up so that it does not contain None and nan
                if (performer is None) or (type(performer) == float):
                    continue

                artist = Artist(name=performer, ignore_sc=False)
                name = performer

                if Artist.objects.filter(name=performer).exists():
                    print performer
                    artist = Artist.objects.get(name=performer)
                # if name in aristsnames retrieve the sc_id: arists.soundcloud_id = id
                elif artist.get_sc_id() != None:
                    print "sc_id=" + str(artist.soundcloud_id)
                    if Artist.objects.filter(soundcloud_id=artist.soundcloud_id).exists():
                        # artist already exists so to link the event we use the existing one
                        artist = Artist.objects.get(soundcloud_id=artist.soundcloud_id)
                    else:
                        # sc id is not in database add artist
                        artist.save()
                else:
                    #we don't have a sc_id check by name
                    if(Artist.objects.filter(name = artist.name).exists()):
                        artist = Artist.objects.get(name=artist.name)
                    else:
                        print artist.name
                        artist.save()

                event.artists.add(artist)
        except RuntimeError, e:
            print e
            print "artist name was %s" % name

        except Exception, e:
            print "an Error happened:"
            print e
            '''
            save = raw_input("Do you wish to continue? type y for yes anything else for no \n")
            if (save != "y"):
                return
            '''

    
if __name__ == '__main__':
    main(1,2,3)
