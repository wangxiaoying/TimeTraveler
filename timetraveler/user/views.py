from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import auth
from django.template import RequestContext

from user.models import *

import simplejson
import hashlib


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

		response['result'] = 'SUCCESS'
		return HttpResponse(simplejson.dumps(response))

	except Exception as e:
		print(e)
		response['result'] = 'FAIL'
		return HttpResponse(simplejson.dumps(response))

@csrf_exempt
def unfollow(request):
	response = {}
	try:
		hero_id = request.POST.get('hero_id')
		user_hero = User.objects.get(id=hero_id)

		FollowRelation.objects.filter(user_hero=user_hero, user_fan=request.user).delete()

		response['result'] = 'SUCCESS'
		return HttpResponse(simplejson.dumps(response))

	except Exception as e:
		print(e)
		response['result'] = 'FAIL'
		return HttpResponse(simplejson.dumps(response))

@csrf_exempt
def getRelationship(request):
	response = {}
	try:
		user_id_1 = request.POST.get('user_1')
		user_id_2 = request.POST.get('user_2')

		user_1 = User.objects.get(id=user_id_1)
		user_2 = User.objects.get(id=user_id_2)

		relation_1 = FollowRelation.objects.filter(user_hero=user_1, user_fan=user_2)
		relation_2 = FollowRelation.objects.filter(user_hero=user_2, user_fan=user_1)

		if len(relation_1) > 0 and len(relation_2) > 0:
			response['relation'] = 'FRIEND'
		elif len(relation_2) > 0:
			response['relation'] = 'HERO'
		elif len(relation_1) > 0:
			response['relation'] = 'FAN'
		else:
			response['relation'] = 'NA'
		return HttpResponse(simplejson.dumps(response))

	except Exception as e:
		print(e)
		response['relation'] = 'FAIL'
		return HttpResponse(simplejson.dumps(response))









