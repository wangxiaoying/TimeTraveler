from django.db import models
from django.contrib.auth.models import User

from event.models import *

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	gender = models.BooleanField(default=False)
	portrait = models.FileField(upload_to='portrait')
	signature = models.CharField(max_length=200)
	credits = models.IntegerField(default=0)

	def __unicode__(self):
		return self.user.username

class UserToken(models.Model):
	user = models.OneToOneField(User)
	token = models.CharField(max_length=200)

class FollowRelation(models.Model):
	user_hero = models.ForeignKey(User, related_name='user_hero')
	user_fan = models.ForeignKey(User, related_name='user_fan')
	has_seen = models.BooleanField(default=False)

	def __unicode__(self):
		return ('user: %s follows user: %s' % (self.user_fan, self.user_hero))

class Message(models.Model):
	user_from = models.ForeignKey(User, related_name='user_message_from')
	user_to = models.ForeignKey(User, related_name='user_message_to')
	message = models.CharField(max_length=200)
	date = models.DateTimeField(auto_now_add=True)
	has_seen = models.BooleanField(default=False)

	def __unicode__(self):
		return self.message

class Notification(models.Model):
	user = models.ForeignKey(User)
	event = models.ForeignKey(Event)
	message = models.CharField(max_length=200)
	has_seen = models.BooleanField(default=False)

	def __unicode__(self):
		return self.message

