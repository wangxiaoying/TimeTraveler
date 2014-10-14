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
from timecapsule.models import *
from timecapsule.forms import *

######################################################
##create new time capsule
@csrf_exempt
def newTimeCapsule(request):
	return render_to_response('newtimecapsule.html', context_instance=RequestContext(request))

@csrf_exempt
def createTimeCapsule(request):
	try:
		u = User.objects.all()[0]
		print (u.id, u.username)
		

		text = request.POST.get('text')
		user_to_id = request.POST.get('user_to')

		if user_to_id is None:
			user_to = request.user
		else:
			user_to = User.objects.get(id=user_to_id)
		user_from = request.user

		image_file = None

		form = TimeCapsuleForm(request.POST, request.FILES)

		if form.is_valid():
			image_file = request.FILES['capsule']

		date_select = time.strptime(request.POST.get('date-to'), '%Y-%m-%d')
		date_to = datetime.fromtimestamp(time.mktime(date_select))

		new_timecapsule = TimeCapsule(user_from=user_from, user_to=user_to, text=text, image=image_file, time_end=date_to)
		new_timecapsule.save()

		return render_to_response('message.html',
			{
				'message': '上传成功',
				'url': '/timecapsule/mysouvenir'
			})


	except Exception as e:
		print (e)
		return render_to_response('message.html',
			{
				'message': '服务器错误',
				'url': '/timecapsule/mysouvenir'
			})

######################################################
##show all recieved time capsule
@csrf_exempt
def mySouvenir(request):
	try:
		capsules = TimeCapsule.objects.filter(user_to=request.user, has_seen=True)

		notis = getNotifications(request.user)
		notifications = notis['notifications']
		new_followers = notis['new_followers']

		return render_to_response('mysouvenir.html',
			{
				'me': request.user,
				'capsules': capsules,
				'notifications': notifications,
				'new_followers': new_followers,
				'user': request.user
			})

	except Exception as e:
		print(e)
		return render_to_response('message.html',
			{
				'message': '服务器错误',
				'url': '/timecapsule/mysouvenir'
			})

######################################################
##show a specific time capsule
@csrf_exempt
def showTimeCapsule(request):
	try:
		if not request.user.is_authenticated():
			return HttpResponseRedirect('/user/index')

		capsule_id = request.GET.get('id')
		capsule = TimeCapsule.objects.get(id=capsule_id)

		if not request.user.id is capsule.user_to.id:
			return render_to_response('message.html',
				{
					'message': '您没有权限访问该时间囊',
					'url': '/event/myspace'
				})

		capsule.has_seen = True
		capsule.save()

		notis = getNotifications(request.user)
		notifications = notis['notifications']
		new_followers = notis['new_followers']

		return render_to_response('showtimecapsule.html',
			{
				'me': request.user,
				'capsule': capsule,
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






























