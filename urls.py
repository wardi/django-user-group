from django.conf.urls.defaults import *

from meetings.feeds import UpcomingMeetings
from django.contrib import admin

# find the installed applications ourselves
admin.autodiscover()


try:
    from feedjack.models import Post
    # content for the Planet OCLUG box
    upcoming_meetings_extra={'planet_oclug':lambda: (
        Post.objects.filter(
            feed__subscriber__site__url='http://planet.oclug.on.ca',
            feed__subscriber__is_active=True,
            feed__is_active=True,
            ).order_by('-date_modified')[:15])}
except ImportError, err:
    # ignore missing feedjack module
    upcoming_meetings_extra={}


# RSS feeds

feeds = {
    'upcoming': UpcomingMeetings,
}


# URLs

urlpatterns = patterns('',
    (r'^$', 
        'meetings.views.upcoming_meetings',
        dict(extra_content=upcoming_meetings_extra)),
        
    (r'^past_meetings/$', 
        'meetings.views.past_meetings'),

    (r'^meeting/(?P<object_id>\d+)/$', 
        'meetings.views.meeting_detail'),

    (r'^location/(?P<object_id>\d+)/$', 
        'meetings.views.location_detail'),
    
    (r'^speaker/(?P<object_id>\d+)/$', 
        'meetings.views.speaker_detail'),

    (r'^image/(?P<path>.+)/$', 
        'meetings.views.view_image'),

    (r'^files/$',
        'meetings.views.list_files'),

    (r'^admin/(.*)$', admin.site.root),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^feeds/(?P<url>.*)/$', 
        'django.contrib.syndication.views.feed', 
        {'feed_dict': feeds}),
)
