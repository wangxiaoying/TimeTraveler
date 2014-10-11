from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):

	def image_file(self, filename):
		url = 'images/users/%s/%s' % (self.user.username, filename)
		return url

	user = models.ForeignKey(User)
	text = models.CharField(max_length=200)
	image_1 = models.FileField(upload_to=image_file)
	image_2 = models.FileField(upload_to=image_file)
	image_3 = models.FileField(upload_to=image_file)
	image_4 = models.FileField(upload_to=image_file)
	image_5 = models.FileField(upload_to=image_file)
	image_6 = models.FileField(upload_to=image_file)
	image_7 = models.FileField(upload_to=image_file)
	image_8 = models.FileField(upload_to=image_file)
	image_9 = models.FileField(upload_to=image_file)
	date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.text

class Comment(models.Model):
	user = models.ForeignKey(User)
	event = models.ForeignKey(Event)
	comment = models.CharField(max_length=200)
	date = models.DateTimeField(auto_now_add=True)
	has_seen = models.BooleanField(default=False)

	def __unicode__(self):
		return self.comment

class Like(models.Model):
	user = models.ForeignKey(User)
	event = models.ForeignKey(Event)
	cancel = models.BooleanField(default=False)
	has_seen = models.BooleanField(default=False)

	def __unicode__(self):
		return ('user: %s likes event: %d' % (self.user.username, self.event.id))