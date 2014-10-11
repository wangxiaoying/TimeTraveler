from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from timetraveler.settings import *

user_patterns = patterns('user.views',
	url(r'^user/index$', 'index'),
	url(r'^user/login$', 'login'),

	url(r'^user/newuser$', 'newuser'),
	url(r'^user/register$', 'register'),
)

event_patterns = patterns('event.views',
	url(r'^event/myspace$', 'myspace'),
	url(r'^event/create$', 'createEvent'),
)

timecapsule_patterns = patterns('timecapsule.views',
	url(r'^timecapsule/new$', 'newTimeCapsule'),
	url(r'^timecapsule/create$', 'createTimeCapsule'),

)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'timetraveler.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': MEDIA_ROOT }),
)+user_patterns+event_patterns+timecapsule_patterns
