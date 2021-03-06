from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from timetraveler.settings import *

user_patterns = patterns('user.views',
    url(r'^$', 'index'),
    url(r'^/index$', 'index'),
	url(r'^user/index$', 'index'),
	url(r'^user/login$', 'login'),
    url(r'^user/logout$', 'logout'),
    url(r'^user/upload_portrait', 'uploadPortrait'),

	url(r'^user/newuser$', 'newuser'),
	url(r'^user/register$', 'register'),

	url(r'^user/logout$', 'logout'),

	url(r'^user/getrelation$', 'getRelationship'),
	url(r'^user/follow$', 'follow'),
	url(r'^user/unfollow$', 'unfollow'),
	url(r'^user/seennewfo$', 'seenNewFollower'),

	url(r'^user/search$', 'searchUser'),
	url(r'^user/getfans$', 'getFans'),
	url(r'^user/getheros$', 'getHeros'),

	url(r'^user/changepassword$', 'changePassword'),
	url(r'^user/editsignature$', 'editSignature'),

	url(r'^user/getbyid$', 'getUserById'),
	url(r'^user/getuserlist$', 'getUserList'),

	url(r'^user/myalbum$', 'myAlbum'),
	url(r'^user/resendemail$', 'resendEmail'),
	url(r'^user/confirmemail$', 'confirmEmail'),
)

event_patterns = patterns('event.views',
	url(r'^event/myspace$', 'myspace'),
	url(r'^event/homepage$', 'homepage'),

	url(r'^event/create$', 'createEvent'),
	url(r'^event/show$', 'showEvent'),

	url(r'^event/newcomment$', 'createComment'),

	url(r'^event/like$', 'likeEvent'),
	url(r'^event/cancellike$', 'cancelLikeEvent'),

	url(r'^event/getmyphotos$', 'getMyPhotos'),
	url(r'^event/getlikephotos$', 'getLikePhotos'),

	url(r'^event/topic$', 'showTopicPage'),

)

timecapsule_patterns = patterns('timecapsule.views',
	url(r'^timecapsule/new$', 'newTimeCapsule'),
	url(r'^timecapsule/create$', 'createTimeCapsule'),

	url(r'^timecapsule/mysouvenir$', 'mySouvenir'),
	
	url(r'^timecapsule/show$', 'showTimeCapsule'),

	url(r'^timecapsule/check$', 'checkTimeCapsule'),
)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'timetraveler.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': MEDIA_ROOT }),
)+user_patterns+event_patterns+timecapsule_patterns
