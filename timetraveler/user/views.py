from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import auth
from django.template import RequestContext
from django.db.models import Q
# from django.core.mail import send_mail

import smtplib
from email.mime.text import MIMEText  
from email.header import Header  

import random, string
import simplejson
import hashlib
import time
from datetime import datetime
from datetime import timezone

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

		user = User.objects.get(username=username)
		if user is not None and user.is_active is False:
			return render_to_response('message.html', 
				{
					'message': '您还没有激活您的邮箱',
					'url': '/user/index',
					'user_id': user.id
				})


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
		user.is_active = False
		user.save()

		token = makeToken(user.id)
		user_token = UserToken.objects.create(user=user, token=token)
		sendEmail(email, token)

		user_profile = UserProfile.objects.create(user=user)
		user_profile.save()

		return render_to_response('message.html', 
				{
					'message': '快去激活你的邮箱吧',
					'url': '/user/index'
				})

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
def confirmEmail(request):
	try:
		token = request.GET.get('token')
		user_id = token.split(':')[0]
		user = User.objects.get(id=user_id)

		true_token = UserToken.objects.get(user=user)
		if token == true_token.token:
			user.is_active = True
			user.save()
			return HttpResponseRedirect('/user/index')
		
		return render_to_response('message.html',
				{
					'message': '该链接不存在或已过期',
					'url': '/user/newuser'
				})

		
	except Exception as e:
		print(e)
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
			response['relation'] = 'friend'
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
##has seen new followers
@csrf_exempt
def seenNewFollower(request):
	response = {}
	try:
		nf_id = request.POST.get('nf_id')

		new_fo_relation = FollowRelation.objects.get(id=nf_id)
		new_fo_relation.has_seen = True
		new_fo_relation.save()

		response['result'] = 'success'
		return HttpResponse(simplejson.dumps(response))

	except Exception as e:
		print(e)
		response['result'] = 'fail'
		return HttpResponse(simplejson.dumps(response))

######################################################
##change password
@csrf_exempt
def changePassword(request):
	try:
		old_password = request.POST.get('old_password')
		new_password = request.POST.get('new_password')

		if request.user.check_password(old_password) is False:
			return render_to_response('message.html',
				{
					'message': '密码错误，重置失败',
					'url': '/event/myspace'
				})

		request.user.set_password(new_password)
		request.user.save()

		return render_to_response('message.html',
			{
				'message': '密码更改成功',
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
##upload portrait
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
					'url': '/event/myspace'
				})

		return render_to_response('message.html',
				{
					'message': '头像上传失败',
					'url': '/event/myspace'
				})
	except Exception as e:
		print (e)
		return render_to_response('message.html',
				{
					'message': '服务器错误',
					'url': '/event/myspace'
				})

######################################################
##search user
@csrf_exempt
def searchUser(request):
	try:
		users = searchUserByKeyword(request.POST.get('search_key_word'))

		notis = getNotifications(request.user)
		notifications = notis['notifications']
		new_followers = notis['new_followers']

		return render_to_response('userlist.html',
			{
				'users': users,
				'me': request.user,
				'notifications': notifications,
				'new_followers': new_followers
			})
		
	except Exception as e:
		print (e)
		return render_to_response('message.html',
				{
					'message': '服务器错误',
					'url': '/event/myspace'
				})

######################################################
##get user fans
@csrf_exempt
def getFans(request):
	try:
		user_id = request.GET.get('user_id')

		user_aim = User.objects.get(id=user_id)

		users = getMyFans(user_aim)

		notis = getNotifications(request.user)
		notifications = notis['notifications']
		new_followers = notis['new_followers']

		return render_to_response('userlist.html',
			{
				'users': users,
				'me': request.user,
				'notifications': notifications,
				'new_followers': new_followers
			})
	except Exception as e:
		print(e)
		return render_to_response('message.html',
			{
				'message': '服务器错误',
				'url': '/event/myspace'
			})

######################################################
##get user heros
@csrf_exempt
def getHeros(request):
	try:
		user_id = request.GET.get('user_id')

		user_aim = User.objects.get(id=user_id)

		users = getMyHeros(user_aim)

		notis = getNotifications(request.user)
		notifications = notis['notifications']
		new_followers = notis['new_followers']

		return render_to_response('userlist.html',
			{
				'users': users,
				'me': request.user,
				'notifications': notifications,
				'new_followers': new_followers
			})
	except Exception as e:
		print(e)
		return render_to_response('message.html',
			{
				'message': '服务器错误',
				'url': '/event/myspace'
			})

######################################################
##get recommend friends
def getRecoFriends(user):
	reco_users = {}
	temp_users = []

	heros = getMyHeros(user)
	for h in heros:
		h_h = getMyHeros(h)
		temp_users = temp_users + list(h_h)

	#temp = {}.fromkeys(temp_users).keys()
	temp = set(temp_users) - set(getMyHeros(user))
	temp.remove(user)

	for t in temp:
		reco_users[t] = temp_users.count(t)

	result = sorted(reco_users.items(), key=lambda d:d[1], reverse = True)
	if len(result) > 5:
		result = result[0:5]

	return result

def getMyFans(user):
	fans_id = FollowRelation.objects.filter(user_hero=user).values('user_fan')
	fans = User.objects.filter(id__in=fans_id)
	return fans

def getMyHeros(user):
	heros_id = FollowRelation.objects.filter(user_fan=user).values('user_hero')
	heros = User.objects.filter(id__in=heros_id)
	return heros

def getMyFriends(user):
	heros_id = FollowRelation.objects.filter(user_fan=user).values('user_hero')
	fans_id = FollowRelation.objects.filter(user_hero=user).values('user_fan')

	heros = User.objects.filter(id__in=heros_id)
	fans = User.objects.filter(id__in=fans_id)

	friends = heros & fans
	return friends

######################################################
##get recommend topics
def getRecoTopics():
	reco_topics = {}
	temp_topics = []

	topics = Topic.objects.all()
	
	for t in topics:
		temp = EventTopic.objects.filter(topic=t)
		reco_topics[t] = temp.count()

	result = sorted(reco_topics.items(), key=lambda d:d[1], reverse = True)

	if len(result) > 5:
		result = result[0:5]

	return result

######################################################
##get notifications
def getNotifications(user):
	response = {}

	now = datetime.now()
	notifications = []

	noti_timecapsule = TimeCapsule.objects.filter(user_to=user, has_seen=False, has_pushed=True)
	for tc in noti_timecapsule:
		new_noti = {}
		new_noti['message'] = '%s于%s送给你了一个时间囊~' % (tc.user_from.username, tc.time_end.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S'))
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

	response['notifications'] = notifications

	noti_followers = []
	new_fs = FollowRelation.objects.filter(user_hero=user, has_seen=False)
	for fr in new_fs:
		new_fo = {}
		new_fo['origin_id'] = fr.id
		new_fo['follower'] = fr.user_fan
		noti_followers.append(new_fo)

	response['new_followers'] = noti_followers

	return response

######################################################
##search user by keywords
def searchUserByKeyword(keyword):
	print(keyword)
	if keyword is None:
		return None
	key_word = keyword.strip()
	users = User.objects.filter(Q(username__icontains=key_word)|Q(email__icontains=key_word))
	return users

######################################################
##get user by id
@csrf_exempt
def getUserById(request):
	response = {}
	try:
		user_id = request.POST.get('user_id')
		user = User.objects.get(id=user_id)

		response['username'] = user.username
		response['portrait'] = user.userprofile.portrait.url

		response['result'] = 'success'
		return HttpResponse(simplejson.dumps(response))
	except Exception as e:
		print(e)
		response['result'] = 'fail'
		return HttpResponse(simplejson.dumps(response))


######################################################
##get user list for timecapsule reciever
@csrf_exempt
def getUserList(request):
	response = {}
	try:
		users = []
		who = request.POST.get('who')
		if who == '1':
			user_list = getMyFriends(request.user)
		elif who == '0':
			user_list = searchUserByKeyword(request.POST.get('keyword'))
		
		for f in user_list:
			temp = {}
			temp['user_id'] = f.id
			temp['username'] = f.username
			temp['portrait'] = f.userprofile.portrait.url
			users.append(temp);
		response['users'] = users
		response['result'] = 'success'
		return HttpResponse(simplejson.dumps(response))
	except Exception as e:
		print(e)
		response['reuslt'] = 'fail'
		return HttpResponse(simplejson.dumps(response))


######################################################
##go to my album
@csrf_exempt
def myAlbum(request):
	if request.user.is_authenticated():
		return render_to_response('myalbum.html', 
			{
				'me': request.user
			})
	else:
		return render_to_response('login.html', context_instance=RequestContext(request))


######################################################
##send email
@csrf_exempt
def resendEmail(request):
	try:
		user_id = request.GET.get('user_id')
		
		user = User.objects.get(id=user_id)
		user_token = UserToken.objects.get(user=user)

		user_token.token = makeToken(user.id)
		user_token.save()
		sendEmail(user.email, user_token.token)

		return HttpResponseRedirect('/user/index')
	except Exception as e:
		print(e)
		return render_to_response('message.html',
			{
				'message': '服务器错误',
				'url': '/event/myspace'
			})

def sendEmail(email_to, token):
	#Sign In  
	subject = 'Time Traveler 账户激活'  
	text = '<a href="http://localhost:8000/user/confirmemail?token='+ str(token) +'">请点此激活您在TimeTraveler的邮箱</a>'

	# msg = MIMEText(text,'plain','utf-8')#中文需参数‘utf-8’，单字节字符不需要
	msg = MIMEText(text,_subtype='html',_charset='gb2312')  
	msg['Subject'] = Header(subject, 'utf-8')  

	smtp = smtplib.SMTP()  
	smtp.connect(SMTP_SERVER)  
	smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)  
	smtp.sendmail(EMAIL_HOST_USER, email_to, msg.as_string())  
	smtp.quit()

######################################################
##edit signature
@csrf_exempt
def editSignature(request):
	response = {}
	try:
		signature = request.POST.get('signature')
		request.user.userprofile.signature = signature
		request.user.userprofile.save()

		response['result'] = 'success'
		return HttpResponse(simplejson.dumps(response))
	except Exception as e:
		print(e)
		response['result'] = 'fail'
		return HttpResponse(simplejson.dumps(response))

######################################################
##generate token
def makeToken(key):
   return str(key) + ':' + hashlib.md5(str(datetime.now()).encode('utf-8')).hexdigest()


