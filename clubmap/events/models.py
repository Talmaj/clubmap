# -*- coding: utf-8 -*-

from django.db import models
import time
import soundcloud 
from collections import Counter
from pygeocoder import Geocoder
from django.db.models import Q
import datetime

client = soundcloud.Client(client_id='5b3cdaac22afb1d743aed0031918a90f')

#Search artists tracks and return his most used genre
def determineGenre(client,sc_id):
    tracks = client.get('users/'+str(sc_id)+'/tracks')
    if not tracks: return '' # if there are no tracks

    _list = []
    for track in tracks: _list.append(track.genre)
    if not _list: return '' # if there are no genres defined for the tracks
    if not list(set(_list))[0]: return '' # if all elements are None
    #print _list

    occur = Counter(_list)
    i = 0
    while (occur.most_common()[i][0] == None or occur.most_common()[i][0] == ''):
        i = i+1
    result = occur.most_common()[i][0]
    return result.encode('utf-8')

class Artist(models.Model):
    name = models.CharField(max_length=200)
    label = models.CharField(max_length=200, blank=True)
    soundcloud_id = models.PositiveIntegerField(null=True,unique=True)
    genres = models.ManyToManyField('Genre',null=True,blank=True)
    ignore_sc = models.BooleanField('Ignore Soundcloud')
    
    def __unicode__(self):
        return 'Artist[ ' + self.name + ', @: ' + self.label + ', ' + str(self.soundcloud_id) + ' ]'
    def get_sc_id(self):
        #try:
        user = client.get('/users', q=self.name)
        #if user is not emtpy assign data
        if(len(user)!=0):
            user = user[0]
            if not(user.website_title == None): self.label = user.website_title
            self.soundcloud_id = user.id
            
            artist_genre = determineGenre(client,user.id)
            try:
                #get id corresponding to genre
                Genre_artist = Genre.objects.get(genre_name=artist_genre)
                #and save it
                self.genre = Genre_artist.id
                
            except Exception, e:
                    #Add Genre to unkown Genres TODO: this is not working quite right yet
                    print "genre not found {}".format(artist_genre)
                    unkown = unkownGenre(name=artist_genre, soundcloud_id=user.id)
                    unkown.save()
        else:
            return None;
'''
TODO:
-Read this:
    http://www.protocolostomy.com/2009/08/21/lessons-learned-while-creating-a-generic-taxonomy-app-for-django/
    doesn't need to be generic
-and this
    https://docs.djangoproject.com/en/dev/ref/models/fields/#manytomany-arguments
-then check again
'''
class Genre(models.Model):
    genre_name = models.CharField(max_length=200,unique=True)
    parent_id = models.ManyToManyField('self')
    
    def __unicode__(self):
        parent = Genre.object.get(id = self.parent_id)
        return 'Genre[ ' + self.genre_name + ', parent: ' + parent.genre_name + ' ]'

'''
Event Model
TODO:
-File uploads not working 
'''  
class EventManager(models.Manager):
    '''
    Today's events
    Returns todays event from now to now + 24h
    '''
    def today(self):
        return self.from_date(datetime.datetime.now())

    '''
    Returns events of a certain day
    '''
    def from_date(self,start):
        end = start + datetime.timedelta(days=1)
        return self.from_range(start,end)
    '''
    Method to specific search events in given range
    returns Events from start to end
    '''
    def from_range(self,start, end):
        return self.filter(Q(event_date_start__range=(start, end)) | Q(event_date_end__range=(start, end)))

    '''
    This weekend
    returns events of upcoming weekend next friday 00:00 till monday 12:00
    '''
    def weekend(self):
        today = datetime.datetime.today();
        if (today.weekday != 4 and  today.weekday != 5 and today.weekday != 6):
            '''
            Today is a weekday find next friday
            '''
            while (today.weekday() != 4):
                today += datetime.timedelta(days=1)
            friday = today;
            monday = friday + datetime.timedelta(days = 3, hours = 12)
            return self.from_range(friday,monday)
        else:
            '''
            During the weekend return the remaining events
            '''
            monday = datetime.datetime.today()
            while(monday.weekday() != 0):
                monday += datetime.timedelta(days=1)
            monday += datetime.timedelta(hours=12)
            start = datetime.datetime.now() 
            return self.from_range(start, monday)


    '''
    This week
    returns events of from current day of week till monday 12:00
    '''
    def week(self):
        start = datetime.datetime.today()
        end = start + datetime.timedelta(days=1, hours=12)
        while (end.weekday() != 0):
            end += datetime.timedelta(days=1)
        return self.from_range(start,end)


class Event(models.Model):
    
    #File gets validated by ImageField if uploaded through backend upload using script must handle validation itself
    def get_image_path(instance, filename):
        sec = str(time.time()).split('.')[0]
        path = '/img/events/%Y/%m/' + sec + '_' + filename
        return path
    
    event_name = models.CharField(max_length=200)
    description = models.TextField(blank = True)
    
    event_date_start = models.DateTimeField('date and time event starts')
    event_date_end = models.DateTimeField('date and time event ends')
    pub_date = models.DateTimeField('dateime when event was added to database',auto_now_add=True)

    price = models.DecimalField(max_digits = 5, decimal_places = 2)

    image = models.ImageField(upload_to ='events/img/', blank = True)

    artists = models.ManyToManyField(Artist, blank=True)
    location = models.ForeignKey('Location')

    fb_id = models.PositiveIntegerField(unique=True, null=True)
    ra_id = models.PositiveIntegerField(unique=True, null=True)

    published = models.BooleanField('Published')
    gay = models.BooleanField('Gay party')

    objects = EventManager()

    def as_dic(self):
        artists = [artist.soundcloud_id for artist in self.artists.all()]
        artists = filter(None, artists)
        return {
            "id" : self.id,
            "name" : self.event_name,
            "location": self.location.location_name,
            "lat" : self.location.latitude,
            "long": self.location.longitude,
            "artists" : artists
        }

    #could use some more love
    def __unicode__(self):
        return 'Event[ ' + self.event_name + ', ' + 'startdate' + ' ]'
    

class Location(models.Model):
    '''
    Define country codes
    '''
    GERMANY = 'DE'
    AUSTRIA = 'AT'
    SLOVENIA = 'SI'
    NETHERLANDS = 'SL'
    UNITEDKINGDOM = 'UK'
    
    COUNTRYS = (
                (GERMANY, 'Deutschland'),
                #(AUSTRIA, 'Österreich'),
                #(SLOVENIA, 'Slovenija'),
                #(NETHERLANDS, 'Nederland'),
                #(UNITEDKINGDOM, 'Great Britian'),
                )
    
    def get_image_path(instance, filename):
        sec = str(time.time()).split('.')[0]
        path = '/img/'+ instance.location_name +'/%Y/%m/' + sec + '_' + filename
        return path
    
    pub_date = models.DateTimeField('dateime location was added to database',auto_now_add=True)

    location_name = models.CharField(max_length=200)
    website = models.CharField(max_length=200, blank=True)
    description = models.TextField()

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    street = models.CharField(max_length=200)
    postal_code = models.PositiveIntegerField()
    city = models.CharField(max_length=200)
    country_code = models.CharField('state', max_length=2, choices = COUNTRYS, default = GERMANY)
    
    image = models.ImageField(upload_to ='events/img/' ,blank=True)

    fb_id = models.PositiveIntegerField(unique=True, null=True)
    ra_id = models.PositiveIntegerField(unique=True, null=True)
    
    published = models.BooleanField('Published')
    
    def setAddress(self, street, postal_code, location_name):
        ## this can be deleted
        '''
        Set name of the street, postal code and venue name.
        '''
        self.street = street
        self.postal_code = postal_code
        self.location_name = location_name

    def __unicode__(self):
        return 'Location[ ' + self.location_name + ', ' + ' coordinates: (' + str(self.latitude) + ', ' + str(self.longitude) + ') ]'
    
    def setCoordinates(self):
        address = self.street + ', ' + self.postal_code + ' ' + self.city
        self.latitude, self.longitude = Geocoder.geocode(address).coordinates

'''
Name Abstraction Class will be used for machine learning
Move this to artist??
'''
class ArtistNames(models.Model):
    name = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist)
    
    
    def __unicode__(self):
        artistRef = Artist.object.get(id = self.artist)
        return 'NameAbstraction[ ' + self.name + '-->' + artistsRef.name + ' ]'

'''
Unknown Genres will be saved here with a reference to the Artistsearch fftw3
'''
class unkownGenre(models.Model):
    name = models.CharField(max_length=200)
    soundcloud_id = models.PositiveIntegerField()
