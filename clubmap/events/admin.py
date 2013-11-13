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
                        'fields' : ('event_date_start', 'event_date_end')
              }),             
    )
    
    filter_horizontal = ('artists',)

class ArtistAdmin(admin.ModelAdmin):
    filter_horizontal = ('genres',)
    form = ScArtistAdminForm
                
    
admin.site.register(Event,EventAdmin)
admin.site.register(Artist, ArtistAdmin)