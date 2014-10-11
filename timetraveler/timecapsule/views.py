from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import auth
from django.template import RequestContext

from user.models import *
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
		text = request.POST.get('text')
		user_to_id = request.POST.get('user_to')

		if user_to_id is None:
			print("it is for myself!")
			user_to = request.user
		else:
			user_to = User.objects.get(id=user_to_id)
		user_from = request.user

		image_file = None

		form = TimeCapsuleForm(request.POST, request.FILES)

		if form.is_valid():
			image_file = request.FILES['capsule']

		#new_timecapsule = TimeCapsule(user_from=user_from, user_to=user_to, text=text, image=image_file)
		u = User.objects.all()[0]
		print (u.id, u.username)
		nt = TimeCapsule(user_from=u, user_to=u, text=text, image=image_file)
		print('test.........')
		#new_timecapsule.save()
		nt.save()
		print('what.........')
		return render_to_response('message.html',
			{
				'message': '上传成功',
				'url': '/timecapsule/mySouvenir'
			})


	except Exception as e:
		print (e)
		return render_to_response('message.html',
			{
				'message': '服务器错误',
				'url': '/timecapsule/mySouvenir'
			})

######################################################
##show all recieved time capsule
# @csrf_exempt
# def mySouvenir(request):
# 	try:

# 	except Exception as e:
# 		print(e)
# 		return render_to_response('message.html',
# 			{
# 				'message': '服务器错误',
# 				'url': '/event/myspace'
# 			})





