from django.db import models
'''
Event Model
TODO:
-Add Field Options for enhanced treatmend in validation and backend, see:
    https://docs.djangoproject.com/en/dev/ref/models/fields/#field-options
-Finish image field
-Implement logic functions

'''
class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_date = models.DateTimeField('datetime event starts')
    pub_date = models.DateTimeField('dateime event was added to database')
    price = models.DecimalField(max_digits = 5, decimal_places = 2)
    description = models.TextField()
    #This one needs a lot of work to be done see:
    #https://docs.djangoproject.com/en/dev/topics/files/
    image = models.ImageField()
    #may need some more thinkin not sure right now
    artists = models.ManyToManyField(Artist)
    genres = models.ManyToManyField(Genre)

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
    parent_id = models.ManyToManyField(Genre)
'''
TODO:
-see Events
'''
class Location(models.Model):
    location_name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    street = models.CharField(max_length=200)
    postal_code = models.PositiveIntegerField()
    city = models.CharField(max_length=200)
    country_code = models.CharField(max_length=2)
    website = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField()

class Artist(modesl.Model):
    name = models.CharField(max_length=200)
    label = models.CharField(may_length=200)
    soundcloud_id = models.PositiveIntegerField()

class ArtistNames(models.Model):
    name = models.CharField(max_length=200)
    artist = models.ManyToManyField(Artist)

    
    
