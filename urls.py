from django.conf.urls.defaults import *
from django.contrib import admin

from meetings.feeds import UpcomingMeetings
from jobs.feeds import JobPostings

from jobs.views import get_postings

# find the installed applications ourselves
admin.autodiscover()


# extra front-page content
upcoming_meetings_extra = {'jobs': lambda: get_postings()[:10]}
try:
    from feedjack.models import Post
    # content for the Planet OCLUG box
    upcoming_meetings_extra['planet_oclug'] = lambda: (
        Post.objects.filter(
            feed__subscriber__site__url='http://planet.oclug.on.ca',
            feed__subscriber__is_active=True,
            feed__is_active=True,
            ).order_by('-date_modified')[:10])
except ImportError, err:
    # ignore missing feedjack module
    pass


# RSS feeds

feeds = {
    'upcoming': UpcomingMeetings,
    'jobs': JobPostings,
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

    (r'^jobs/$',
        'jobs.views.list_postings'),

    (r'^posting/(?P<posting_id>\d+)/$',
        'jobs.views.view_posting'),

    (r'^posting/new/nospam/$',
        'jobs.views.new_posting'),

    (r'^posting/edit/(?P<posting_id>\d+)/(?P<hash>[\dabcdef]+)/$',
        'jobs.views.edit_posting'),

    (r'^admin/(.*)$', admin.site.root),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^feeds/(?P<url>.*)/$', 
        'django.contrib.syndication.views.feed', 
        {'feed_dict': feeds}),
)
