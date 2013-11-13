from events.models import Genre
from django.contrib import messages
from django.forms import ModelForm, ValidationError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from collections import Counter
import soundcloud

client = soundcloud.Client(client_id='5b3cdaac22afb1d743aed0031918a90f')

#Search artists tracks and return his most used genre
def determineGenre(client,sc_id):
    tracks = client.get('/tracks', )
    list = []
    for track in tracks: list.append(track.genre)
    occur = Counter(list)
    return occur.most_common(1)[0][0]
   
class ScArtistAdminForm(ModelForm):
    def clean(self):
        #should we use soundcloud to get more data
        if (self.cleaned_data['ignore_sc']):
            super(ScArtistAdminForm, self).clean()
            return self.cleaned_data
        
        ##check if a Field was left blank default is to use soundcloud
        if not (False):
            #retrieve missing data from sc

            user = client.get('/users', q=self.cleaned_data['name'])
            #if user is not emtpy assign data
            if(len(user)!=0):
                user = user[0]
                if not(user.website_title == None): self.cleaned_data['label'] = user.website_title
                self.cleaned_data['soundcloud_id'] = user.id
                
                artist_genre = determineGenre(client,user.id)
                try:
                    #get id corresponding to genre
                    Genre_artist = Genre.objects.get(genre_name=artist_genre)
                    #and save it
                    self.cleaned_data['genre'] = Genre_artist.id
                    
                except (MultipleObjectsReturned, ObjectDoesNotExist):
                    warning = 'No genre was added because no or multiple key were found for {}'.format(artist_genre)
                    #messages.warning(request, warning)

        super(ScArtistAdminForm, self).clean()
        return self.cleaned_data