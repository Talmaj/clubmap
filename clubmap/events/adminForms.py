from events.models import Genre, unkownGenre
from django.contrib import messages
from django.forms import ModelForm, ValidationError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from collections import Counter
import soundcloud

client = soundcloud.Client(client_id='5b3cdaac22afb1d743aed0031918a90f')
##This might be legacy code

#Search artists tracks and return his most used genre
def determineGenre(client,sc_id):
    tracks = client.get('users/'+str(sc_id)+'/tracks')
    list = []
    for track in tracks: list.append(track.genre)
    occur = Counter(list)
    i = 0
    while (occur.most_common()[i][0] == None or occur.most_common()[i][0] == ''):
        i = i+1
    result = occur.most_common()[i][0]
    return result.encode('utf-8')
   
class ScArtistAdminForm(ModelForm):
    def clean(self):
        #should we use soundcloud to get more data
        if (self.cleaned_data['ignore_sc']):
            super(ScArtistAdminForm, self).clean()
            return self.cleaned_data
        
        ##check if a Field was left blank default is to use soundcloud
        if not (self.cleaned_data['ignore_sc']):
            #retrieve missing data from sc
            try:
                user = client.get('/users/jdshf/tracks', q=self.cleaned_data['name'])
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
                            #Add Genre to unkown Genres TODO: this is not working quite right yet
                            unkown = unkownGenre(name=artist_genre, soundcloud_id=user.id)
                            #unkown.save()
            except Exception as ex:
                raise ValidationError(
                    ('An error occured searching Soundcloud: %(value)s, Arguments%(args)s'),
                    code='invalid',
                    params={'value': type(ex).__name__,
                            'args':  ex.args
                            },
                )
        super(ScArtistAdminForm, self).clean()
        return self.cleaned_data
##TODO add Location Admin Form