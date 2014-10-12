from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import auth
from django.template import RequestContext

import time
from datetime import datetime
import simplejson

from user.models import *
from user.views import *
from event.models import *
from timecapsule.models import *
from event.forms import *
from utils import *

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
	response = {}
	try:
		if not request.user.is_authenticated():
			return HttpResponseRedirect('/user/index')
		text = request.POST.get('text')
		event_id = request.POST.get('event_id')

		event = Event.objects.get(id=event_id)
		
		comment = Comment(user=request.user, event=event, comment=text)
		comment.save()

		response['result'] = 'success'
		response['comment'] = comment.comment
		response['username'] = request.user.username
		if request.user.userprofile.portrait:
			response['portrait'] = request.user.userprofile.portrait.url
		else:
			response['portrait'] = getDefaultPortrait()
		response['date'] = comment.date.strftime('%Y-%m-%d')

		#create notifications
		message = '%s于%s对您发言过的时间碎片做了评论~' % (request.user.username, comment.date.strftime('%y年%m月%d日'))
		user_to = Comment.objects.filter(event=event).values('user').distinct()

		for user_id in user_to:
			u = User.objects.get(id=user_id['user'])
			if u != request.user and u != event.user:
				new_noti = Notification(user=u, event=event, message=message)
				new_noti.save()

		if request.user != event.user:
			print('haha not me')
			message0 = '%s于%s对评论了您的时间碎片~' % (request.user.username, comment.date.strftime('%y年%m月%d日'))
			new_noti = Notification(user=event.user, event=event, message=message0)
			new_noti.save()

		return HttpResponse(simplejson.dumps(response))

	except Exception as e:
		print(e)
		response['result'] = 'fail'

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

######################################################
##show a specific event
@csrf_exempt
def showEvent(request):
	try:
		if not request.user.is_authenticated():
			return HttpResponseRedirect('/user/index')

		event_id = request.GET.get('id')
		event = Event.objects.get(id=event_id)
		comments = Comment.objects.filter(event=event)

		news = {}
		news['event'] = event
		news['comments'] = comments

		Notification.objects.filter(event=event, user=request.user).update(has_seen=True)
		notifications = getNotifications(request.user)

		return render_to_response('showevent.html',
			{
				'news': news,
				'notifications': notifications,
				'user': request.user
			})

	except Exception as e:
		print(e)
		return render_to_response('message.html',
			{
				'message': '服务器错误',
				'url': '/event/myspace'
			})
















