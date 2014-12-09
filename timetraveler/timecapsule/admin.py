from django.contrib import admin
from django.contrib.auth.models import User
from timecapsule.models import *

class TimeCapsuleAdmin(admin.ModelAdmin):
	list_display = ('id', 'user_from', 'user_to', 'time_start', 'time_end', 'text', 'image', 'has_seen')


admin.site.register(TimeCapsule, TimeCapsuleAdmin)
