from django.contrib import admin
from events.models import Event, Location, Artist
from django.contrib import messages
from events.adminForms import ScArtistAdminForm

class EventAdmin(admin.ModelAdmin):
    fieldsets = (
              ('General Information', {
                        'fields': ('event_name', 'image', 'price', 'description', 'location', 'artists')
              }),
              ('Date Information', {
                        'fields':  ('event_date_start', 'event_date_end')
              }),             
    )
    
    filter_horizontal = ('artists',)

class ArtistAdmin(admin.ModelAdmin):
    filter_horizontal = ('genres',)
    form = ScArtistAdminForm
    
class LocationAdmin(admin.ModelAdmin):
    fieldsets= (
                ('General Information', {
                            'fields' : ('location_name', 'street', 'postal_code', 'city', 'country_code', 'description', 'image', 'website' )
                }),
                ('Geocoding', {
                        'fields': (('latitude', 'longitude'),)
                })
    )
    
admin.site.register(Event,EventAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Location,LocationAdmin)