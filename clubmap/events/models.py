# -*- coding: utf-8 -*-

from django.db import models
import time

class Artist(models.Model):
    name = models.CharField(max_length=200)
    label = models.CharField(max_length=200)
    soundcloud_id = models.PositiveIntegerField()
    
    def __unicode__(self):
        return 'Artist[ ' + self.name + ', @: ' + self.label + ', ' + self.soundcloud_id + ' ]'
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
    genre_name = models.CharField(max_length=200)
    parent_id = models.ManyToManyField('self')
    
    def __unicode__(self):
        parent = Genre.object.get(id = self.parent_id)
        return 'Genre[ ' + self.genre_name + ', parent: ' + parent.genre_name + ' ]'

'''
Event Model
TODO:
-Add Field Options for enhanced treatmend in validation and backend, see:
    https://docs.djangoproject.com/en/dev/ref/models/fields/#field-options
-Finish image field :: DONE
-Implement logic functions

'''  
class Event(models.Model):
    
    #File gets validated by ImageField if uploaded through backend upload using script must handle validation itself
    def get_image_path(instance, filename):
        sec = str(time.time()).split('.')[0]
        path = '/img/events/%Y/%m/' + sec + '_' + filename
        return path
    
    event_name = models.CharField(max_length=200)
    event_date = models.DateTimeField('datetime event starts')
    pub_date = models.DateTimeField('dateime event was added to database',auto_now_add=True)
    price = models.DecimalField(max_digits = 5, decimal_places = 2)
    description = models.TextField()
    #This one needs a lot of work to be done see:
    #https://docs.djangoproject.com/en/dev/topics/files/
    image = models.ImageField(upload_to =lambda self, fname:self.get_image_path(fname))
    #may need some more thinkin not sure right now
    artists = models.ManyToManyField(Artist)
    genres = models.ManyToManyField(Genre)
    
    #could use some more love
    def __unicode__(self):
        return 'Event[ ' + self.event_name + ', ' + self.event_date + ' ]'
    

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
    latitude = models.FloatField()
    longitude = models.FloatField()
    street = models.CharField(max_length=200)
    postal_code = models.PositiveIntegerField()
    city = models.CharField(max_length=200)
    country_code = models.CharField(max_length=2, choices = COUNTRYS, default = GERMANY)
    website = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to =lambda self, fname:self.get_image_path(fname))
    
    def __unicode__(self):
        return 'Location[ ' + self.location_name + ', ' + self.location_date + ', coordinates: (' + str(self.latitude) + ', ' + str(self.longitude) + ') ]'

'''
Name Abstraction Class will be used for machine learning
'''
class ArtistNames(models.Model):
    name = models.CharField(max_length=200)
    artist = models.ManyToManyField(Artist)
    
    
    def __unicode__(self):
        artistRef = Artist.object.get(id = self.artist)
        return 'NameAbstraction[ ' + self.name + '-->' + artistsRef.name + ' ]'

    
    
