from django.contrib import admin
from django.contrib.auth.models import User
from user.models import *

class UserProfileAdmin(admin.ModelAdmin):
    #fields = ['gender', 'portrait', 'signature']
    list_display = ('id', 'user', 'gender', 'portrait', 'signature')

class FollowRelationAdmin(admin.ModelAdmin):
	#fields = ['user_hero', 'user_fan']
	list_display = ('id', 'user_hero', 'user_fan')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(FollowRelation, FollowRelationAdmin)
