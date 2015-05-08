#Here is defined the function invoked in the authentication pipeline
#which triggers the user information retrieval from fb/sc
from models import userFollows, lastUpdateLikes, Artist
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
import social
import soundcloud
#from social.apps.django_app.default import user_social_auth

LAST_RETRIEVAL_INTERVAL = 1 #1 day

def retrieve_facebook_likes(backend, id_us, token):
	music_likes_data = backend.get_json(
			'https://graph.facebook.com/%s/music?fields=name,created_time' % id_us,
			params = {'access_token': token}
		)
	music_likes = []
	while 'next' in music_likes_data['paging']:
		for music_like in music_likes_data['data']:
			#music_like['created_time'] = datetime.strptime(music_like['created_time'],"%Y-%m-%dT%H:%M:%S+0000")#2010-12-31T14:15:45+0000")
			music_likes.append(music_like)
		music_likes_data = backend.get_json(
			music_likes_data['paging']['next']
			)

	artists = []
	for like in music_likes:
		try:
			artists.append(Artist.objects.get(name__icontains=like['name']))
		except Artist.MultipleObjectsReturned:
			try:
				artists.append(Artist.objects.get(name__contains=like['name']))
			except Exception, e:
				pass
		except Artist.DoesNotExist:
			pass
	return artists

def retrieve_soundcloud_followings(id_us,access_token):
	client = soundcloud.Client(access_token=access_token)
	music_likes = client.get('/me/followings')
	music_likes = [{'id':following.obj['id'], 'username':following.obj['username']} for following in music_likes]
	artists = Artist.objects.filter(soundcloud_id__in=[entry['id'] for entry in music_likes])
	return artists

def link_user_likes(user,artists):
	for ar in artists:
		relation, created = userFollows.objects.get_or_create(user=user,artist=ar)

def update_likes_and_link(backend, user, id_provider, access_token):
	#Get the user from the authentication pipeline
	#invoke network API to get likes
	artists=[]
	if backend.name == 'facebook':
		artists=retrieve_facebook_likes(backend,id_provider,access_token)
	if backend.name == 'soundcloud':
		artists=retrieve_soundcloud_followings(id_provider,access_token)
	#Store the new information in the userFollows table
	#Look for coincidences against Artist table, in order to leave out SC user who aren't djs (e.g friends you are following)
	link_user_likes(user,artists)

def update_likes_logic(backend,user,id_provider,access_token):
	now = timezone.now()
	try:
		user_last_retrieval = lastUpdateLikes.objects.get(user=user)
		tdelta = now-timedelta(days=LAST_RETRIEVAL_INTERVAL)
		if tdelta > user_last_retrieval.last_update:
			update_likes_and_link(backend,user,id_provider, access_token)
			user_last_retrieval.last_update = now
			user_last_retrieval.save()
	except lastUpdateLikes.DoesNotExist:
		update_likes_and_link(backend,user,id_provider, access_token)
		latest_retrieval = lastUpdateLikes(user=user,last_update=now)
		latest_retrieval.save()

def update_likes(backend, user, response, *args, **kwargs):
	update_likes_logic(backend,user,response['id'],response['access_token'])
	

def update_likes_index_view_wrapper(request):
	#mirar la id de sesion para sacar el backend
	#request.user.social_auth.get
	#update_likes(backend,request.user,None,None,None)
	user = request.user.social_auth.get(user=request.user)
	provider = request.user.social_auth.get(provider=user.provider)
	backend = provider.get_backend_instance()
	update_likes_logic(backend,request.user,user.id,user.access_token)




