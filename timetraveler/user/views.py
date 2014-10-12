from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import auth
from django.template import RequestContext

import simplejson
import hashlib
import time
from datetime import datetime

from user.models import *
from user.forms import *
from timecapsule.models import *
from utils import *

######################################################
##login & register & logout

@csrf_exempt
def index(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/event/myspace')
	else:
		return render_to_response('login.html', context_instance=RequestContext(request))

@csrf_exempt
def login(request):
	try:
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = auth.authenticate(username=username, password=password)

		if user is not None:
			auth.login(request, user)
			if user.is_superuser is True:
				return HttpResponseRedirect('/user/admin')
			else:
				return HttpResponseRedirect('/event/myspace')
		else:
			return render_to_response('message.html', 
				{
					'message': '用户名密码错误',
					'url': '/user/index'
				})

	except Exception as e:
		print(e)
		return render_to_response('message.html',
			{
				'message': '服务器错误',
				'url': '/user/index'
			})

@csrf_exempt
def newuser(request):
	if request.user.is_authenticated():
		return render_to_response('register.html')
	else:
		return render_to_response('register.html')

@csrf_exempt
def register(request):
	try:
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')

		user = User.objects.create_user(username=username, email=email, password=password)
		user.save()

		user_profile = UserProfile.objects.create(user=user)
		user_profile.save()

		user = auth.authenticate(username=username, password=password)
		auth.login(request, user)
		return HttpResponseRedirect('/user/index')

	except Exception as e:
		print(e)
		name_of_exception = e.__class__.__name__
		if name_of_exception is 'IntegrityError':
			return render_to_response('message.html',
				{
					'message': '用户名已存在',
					'url': '/user/newuser'
				})
		else:
			return render_to_response('message.html',
				{
					'message': '服务器错误',
					'url': '/user/newuser'
				})

@csrf_exempt
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/user/index')

######################################################
##relation & follow & unfollow
@csrf_exempt
def follow(request):
	response = {}
	try:
		hero_id = request.POST.get('hero_id')
		user_hero = User.objects.get(id=hero_id)

		follow_relation = FollowRelation.objects.create(user_hero=user_hero, user_fan=request.user)
		follow_relation.save()

		response['result'] = 'success'
		return HttpResponse(simplejson.dumps(response))

	except Exception as e:
		print(e)
		response['result'] = 'fail'
		return HttpResponse(simplejson.dumps(response))

@csrf_exempt
def unfollow(request):
	response = {}
	try:
		hero_id = request.POST.get('hero_id')
		user_hero = User.objects.get(id=hero_id)

		FollowRelation.objects.filter(user_hero=user_hero, user_fan=request.user).delete()

		response['result'] = 'success'
		return HttpResponse(simplejson.dumps(response))

	except Exception as e:
		print(e)
		response['result'] = 'fail'
		return HttpResponse(simplejson.dumps(response))

@csrf_exempt
def getRelationship(request):
	response = {}
	try:
		user_id = request.POST.get('user_id')

		if user_id == str(request.user.id):
			response['relation'] = 'myself'
			response['result'] = 'success'
			return HttpResponse(simplejson.dumps(response))

		user_aim = User.objects.get(id=user_id)

		relation_1 = FollowRelation.objects.filter(user_hero=request.user, user_fan=user_aim)
		relation_2 = FollowRelation.objects.filter(user_hero=user_aim, user_fan=request.user)

		if len(relation_1) > 0 and len(relation_2) > 0:
			response['relation'] = 'fiend'
		elif len(relation_2) > 0:
			response['relation'] = 'hero'
		elif len(relation_1) > 0:
			response['relation'] = 'fan'
		else:
			response['relation'] = 'na'
		response['result'] = 'success'
		return HttpResponse(simplejson.dumps(response))

	except Exception as e:
		print(e)
		response['result'] = 'fail'
		return HttpResponse(simplejson.dumps(response))

######################################################
## upload portrait

@csrf_exempt
def uploadPortrait(request):
	try:
		form = PortraitForm(request.POST, request.FILES)

		portrait = None
		if form.is_valid():
			portrait = request.FILES['portrait']

		if portrait is not None:
			up = UserProfile.objects.get(user=request.user)
			up.portrait = portrait
			up.save()
			return render_to_response('message.html',
				{
					'message': '头像更改成功',
					'url': '/'
				})

		return render_to_response('message.html',
				{
					'message': '头像上传失败',
					'url': '/'
				})
	except Exception as e:
		print (e)
		return render_to_response('message.html',
				{
					'message': '服务器错误',
					'url': '/'
				})


######################################################
##get notifications
def getNotifications(user):
	now = datetime.now()
	notifications = []
	# noti_follow = FollowRelation.objects.filter(user_hero=request.user, have_seen=False)
	noti_timecapsule = TimeCapsule.objects.filter(user_to=user, time_end__lt=now, has_seen=False)

	for tc in noti_timecapsule:
		new_noti = {}
		new_noti['message'] = '%s于%s送给你了一个时间囊~' % (tc.user_from.username, tc.time_end.strftime('%y年%m月%d日'))
		new_noti['type'] = 'TC'
		new_noti['origin_id'] = tc.id
		notifications.append(new_noti)

	noti_comlike = Notification.objects.filter(user=user, has_seen=False)
	for cl in noti_comlike:
		new_noti = {}
		new_noti['message'] = cl.message
		new_noti['type'] = 'CL'
		new_noti['origin_id'] = cl.event.id
		notifications.append(new_noti)

	return notifications








