from django.contrib import admin
from django.contrib.auth.models import User
from event.models import *

class EventAdmin(admin.ModelAdmin):
	def comments(self, obj):
		length = len(Comment.objects.filter(event=obj))
		if 0 == length:
			return 0
		return '<a href="/admin/event/comment/?event__id__exact=%d">%d</a>' % (obj.id, length)
	comments.allow_tags = True
	comments.short_description = 'comments'
	list_display = ('id', 'text', 'user', 'comments', 'image_1', 'date')
	# list_display = ('id', 'text', 'user', 'image_1', 'date')
	list_filter = ['date']
	search_fields = ['text', 'user__username']

class CommentAdmin(admin.ModelAdmin):
	list_display = ('id', 'event', 'comment', 'date')
	list_filter = ['date']
	search_fields = ['=event__id']

class TopicAdmin(admin.ModelAdmin):
	def events(self, obj):
		result = '<a href="/admin/event/event/?id__in='
		temp_id = EventTopic.objects.filter(topic=obj).values('event')
		if 0 == len(temp_id):
			return 0
		for i in temp_id:
			result += str(i['event']) + ','
		result = result[:-1]
		result += '">%d</a>' % len(temp_id)
		return result
	events.allow_tags = True
	events.short_description = 'events'
	list_display = ('id', 'topic', 'events', 'date')
	list_filter = ['date']
	search_fields = ['topic']

admin.site.register(Event, EventAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Topic, TopicAdmin)