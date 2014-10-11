from django.db import models
from django.contrib.auth.models import User

def timecapsule_file(self, filename):
	url = 'images/timecapsule/%s/%s' % (self.user_to.username, filename)
	return url

class TimeCapsule(models.Model):
	user_from = models.ForeignKey(User, related_name='user_timecapsule_from')
	user_to = models.ForeignKey(User, related_name='user_timecapsule_to')
	time_start = models.DateTimeField(auto_now_add=True)
	time_end = models.DateTimeField(auto_now_add=True)
	text = models.CharField(max_length=200)
	image = models.FileField(upload_to=timecapsule_file)
	has_seen = models.BooleanField(default=False)
