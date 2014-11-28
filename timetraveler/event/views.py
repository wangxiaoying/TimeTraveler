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

		#pick up topics
		temp_vec = text.split('#')
		for i in range(1, len(temp_vec)-1):
			if i % 2 is not 0 and temp_vec[i] is not '':
				topic, created = Topic.objects.get_or_create(topic=temp_vec[i])
				event_topic = EventTopic.objects.get_or_create(event=new_event, topic=topic)

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
		response['user_id'] = request.user.id
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
			message0 = '%s于%s对评论了您的时间碎片~' % (request.user.username, comment.date.strftime('%y年%m月%d日'))
			new_noti = Notification(user=event.user, event=event, message=message0)
			new_noti.save()

		return HttpResponse(simplejson.dumps(response))

	except Exception as e:
		print(e)
		response['result'] = 'fail'
		return HttpResponse(simplejson.dumps(response))

######################################################
##show myspace
@csrf_exempt
def myspace(request):
	try:
		if not request.user.is_authenticated():
			return HttpResponseRedirect('/user/index')

		notis = getNotifications(request.user)
		notifications = notis['notifications']
		new_followers = notis['new_followers']

		users = FollowRelation.objects.filter(user_fan=request.user).values('user_hero')
		# users.append(request.user)

		news = []
		# events = Event.objects.all().order_by('-date')
		events = Event.objects.filter(Q(user__in=users)|Q(user=request.user)).order_by('-date')
		my_events = []
		for event in events:
			if event.user == request.user:
				my_events.append(event)
			new_news = {}
			new_news['event'] = event
			comments = Comment.objects.filter(event=event)
			new_news['comments'] = comments
			like, created = Like.objects.get_or_create(user=request.user, event=event)
			if created:
				like.is_canceled = True
				like.save()
			new_news['like'] = not like.is_canceled
			news.append(new_news)

		my_fans = FollowRelation.objects.filter(user_hero=request.user)
		my_heros = FollowRelation.objects.filter(user_fan=request.user)

		return render_to_response('myspace.html', 
			{
				'me': request.user,
				'news': news, 
				'user': request.user, 
				'notifications': notifications,
				'new_followers': new_followers,
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
##user homepage
@csrf_exempt
def homepage(request):
	try:
		user_id = request.GET.get('user_id')
		user_aim = User.objects.get(id=user_id)

		notis = getNotifications(request.user)
		notifications = notis['notifications']
		new_followers = notis['new_followers']

		my_fans = FollowRelation.objects.filter(user_hero=user_aim)
		my_heros = FollowRelation.objects.filter(user_fan=user_aim)

		news = []
		events = Event.objects.filter(user=user_aim)
		for event in events:
			new_news = {}
			new_news['event'] = event
			comments = Comment.objects.filter(event=event)
			new_news['comments'] = comments
			like, created = Like.objects.get_or_create(user=request.user, event=event)
			if created:
				like.is_canceled = True
				like.save()
			new_news['like'] = not like.is_canceled
			news.append(new_news)

		reco_friends = getRecoFriends(request.user)
		# print(type(reco_friends))
		# for rf in reco_friends:
		# 	print(type(rf))
		# 	print(rf)

		return render_to_response('myspace.html',
			{
				'me': request.user,
				'news': news,
				'user': user_aim,
				'notifications': notifications,
				'new_followers': new_followers,
				'my_events': events,
				'heros': my_heros,
				'fans': my_fans,
				'reco_friends': reco_friends,
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
		like, created = Like.objects.get_or_create(user=request.user, event=event)
		if created:
			like.is_canceled = True
			like.save()

		news = {}
		news['event'] = event
		news['comments'] = comments
		news['like'] = not like.is_canceled


		Notification.objects.filter(event=event, user=request.user).update(has_seen=True)

		notis = getNotifications(request.user)
		notifications = notis['notifications']
		new_followers = notis['new_followers']

		return render_to_response('showevent.html',
			{
				'me': request.user,
				'news': news,
				'notifications': notifications,
				'new_followers': new_followers,
				'user': request.user
			})

	except Exception as e:
		print(e)
		return render_to_response('message.html',
			{
				'message': '服务器错误',
				'url': '/event/myspace'
			})

######################################################
##like a event
@csrf_exempt
def likeEvent(request):
	response = {}
	try:
		if not request.user.is_authenticated():
			return HttpResponseRedirect('/user/index')

		event_id = request.POST.get('event_id')
		event = Event.objects.get(id=event_id)
		print(event_id)
		
		like = Like.objects.get(user=request.user, event=event)
		like.is_canceled = False
		like.save()

		print(like.is_canceled)
		print('like')

		response['result'] = 'success'
		return HttpResponse(simplejson.dumps(response))

	except Exception as e:
		response['result'] = 'fail'
		return HttpResponse(simplejson.dumps(response))

######################################################
##cancel like a event
@csrf_exempt
def cancelLikeEvent(request):
	response = {}
	try:
		print('cancle')
		if not request.user.is_authenticated():
			return HttpResponseRedirect('/user/index')

		event_id = request.POST.get('event_id')
		event = Event.objects.get(id=event_id)

		like = Like.objects.get(user=request.user, event=event)
		like.is_canceled = True
		like.save()

		
		print(like.is_canceled)

		response['result'] = 'success'
		return HttpResponse(simplejson.dumps(response))

	except Exception as e:
		print(e)
		response['result'] = 'fail'
		return HttpResponse(simplejson.dumps(response))

######################################################
##my album related
@csrf_exempt
def getMyPhotos(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/user/index')

	photos = []
	events = Event.objects.filter(user=request.user)
	
	for e in events:
		temp = {}
		temp['url'] = e.image_1.url
		temp['id'] = e.id
		photos.append(temp)

	return render_to_response('gallery.html',
		{
			'photos': photos,
			'message': '你的相册还没有图片，快去发布新动态吧！',
			'me': request.user
		})

@csrf_exempt
def getLikePhotos(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/user/index')

	photos = []
	event_id = Like.objects.filter(user=request.user, is_canceled=False).values('event')
	events = Event.objects.filter(id__in=event_id)

	for e in events:
		temp = {}
		temp['url'] = e.image_1.url
		temp['id'] = e.id
		photos.append(temp)

	return render_to_response('gallery.html',
		{
			'photos': photos,
			'message': '你喜欢的相册还是空的，快去给你喜欢的图片点个赞吧！',
			'me': request.user
		})

######################################################
##show topic page
@csrf_exempt
def showTopicPage(request):
	try:
		topic_id = request.GET.get('topic_id')

		topic = Topic.objects.get(id=topic_id)
		event_ids = EventTopic.objects.filter(topic=topic).distinct().values('event')
		events = Event.objects.filter(id__in=event_ids).order_by('-date')

		news = []
		for event in events:
			new_news = {}
			new_news['event'] = event
			comments = Comment.objects.filter(event=event)
			new_news['comments'] = comments
			like, created = Like.objects.get_or_create(user=request.user, event=event)
			if created:
				like.is_canceled = True
				like.save()
			new_news['like'] = not like.is_canceled
			news.append(new_news)

		my_fans = FollowRelation.objects.filter(user_hero=request.user)
		my_heros = FollowRelation.objects.filter(user_fan=request.user)

		notis = getNotifications(request.user)
		notifications = notis['notifications']
		new_followers = notis['new_followers']

		return render_to_response('topic.html',
			{
				'topic': topic.topic,
				'me': request.user,
				'news': news, 
				'user': request.user, 
				'notifications': notifications,
				'new_followers': new_followers,
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









