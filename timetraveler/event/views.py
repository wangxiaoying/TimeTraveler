from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import auth
from django.template import RequestContext

import time
from datetime import datetime

from user.models import *
from user.views import *
from event.models import *
from timecapsule.models import *
from event.forms import *

######################################################
##create new event
@csrf_exempt
def createEvent(request):
	try:
		if not request.user.is_authenticated():
			return HttpResponseRedirect('/user/index')

		text = request.POST.get('text')

		#handle image upload

		image_file = None

		form = EventImagesForm(request.POST, request.FILES)
		if form.is_valid():
			image_file = request.FILES['images']

		new_event = Event(user=request.user, text=text, image_1=image_file)
		new_event.save()

		return render_to_response('message.html',
			{
				'message': '上传成功',
				'url': '/event/myspace'
			})

	except Exception as e:
		print(e)
		return render_to_response('message.html',
			{
				'message': '服务器错误',
				'url': '/event/myspace'
			})

######################################################
##create new comment
@csrf_exempt
def createComment(request):
	try:
		print ('aa')
	except Exception as e:
		print(e)
		return render_to_response('message.html',
			{
				'message': '服务器错误',
				'url': '/event/myspace'
			})

######################################################
##show myspace
@csrf_exempt
def myspace(request):
	try:
		if not request.user.is_authenticated():
			return HttpResponseRedirect('/user/index')

		notifications = getNotifications(request.user)
		profile = request.user.userprofile

		news = []
		events = Event.objects.all().order_by('-date')
		my_events = []
		for event in events:
			if event.user == request.user:
				my_events.append(event)
			new_news = {}
			new_news['event'] = event
			new_news['user_profile'] = event.user.userprofile
			comments = Comment.objects.filter(event=event)
			new_news['comments'] = comments
			news.append(new_news)

		my_fans = FollowRelation.objects.filter(user_hero=request.user)
		my_heros = FollowRelation.objects.filter(user_fan=request.user)

		return render_to_response('myspace.html', 
			{
				'news': news, 
				'user': request.user, 
				'notifications': notifications,
				'profile': profile,
				'my_events': my_events,
				'heros': my_heros,
				'fans': my_fans,
			}, context_instance=RequestContext(request))
	except Exception as e:
		print(e)
		return render_to_response('message.html',
			{
				'message': '服务器错误',
				'url': '/event/myspace'
			})







