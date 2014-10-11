from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import auth

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
		profile = UserProfile.objects.get(user=request.user)

		news = []
		events = Event.objects.all()
		for event in events:
			new_news = {}
			new_news['event'] = event
			profile = UserProfile.objects.get(user=event.user)
			new_news['user_profile'] = profile
			comments = Comment.objects.filter(event=event)
			new_news['comments'] = comments
			news.append(new_news)


		return render_to_response('myspace.html', 
			{
				'news': news, 
				'user': request.user, 
				'notifications': notifications,
				'profile': profile
			})
	except Exception as e:
		print(e)
		return render_to_response('message.html',
			{
				'message': '服务器错误',
				'url': '/event/myspace'
			})







