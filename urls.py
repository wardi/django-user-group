from django.conf.urls.defaults import *

from meetings.models import Meeting, Location, Speaker, Announcement
from meetings.feeds import UpcomingMeetings

import datetime


# show meetings that have not yet finished on the upcoming page
# and the rest on the past meetings page.  A meeting is considered
# "done" 2 hours after it starts.

def now_less_meeting_length():
    return datetime.datetime.now() - datetime.timedelta(hours=2)


upcoming_meetings = {
    'queryset': Meeting.objects.filter(visible=True,
        date__gte=now_less_meeting_length).order_by("date"),
    'template_name': 'meetings/upcoming.html',
    'allow_empty': True,
    'extra_context': {
        'announcements':
            lambda: Announcement.objects.filter(visible=True),
        'recent':
            lambda: Meeting.objects.filter(visible=True,
        date__lt=now_less_meeting_length).order_by("-date")[:1],
    }
}

past_meetings = {
    'queryset': Meeting.objects.filter(visible=True,
        date__lt=now_less_meeting_length),
    'template_name': 'meetings/past.html',
    'allow_empty': True,
    'paginate_by': 20,
    'extra_context': {
        'recent':
            lambda: Meeting.objects.filter(visible=True,
        date__lt=now_less_meeting_length).order_by("-date")[:5],
    }
}


# RSS feeds

feeds = {
    'upcoming': UpcomingMeetings,
}


# URLs

urlpatterns = patterns('',
    (r'^$', 
        'django.views.generic.list_detail.object_list', 
        upcoming_meetings),
        
    (r'^past_meetings/$', 
        'django.views.generic.list_detail.object_list',
        past_meetings),

    (r'^meeting/(?P<object_id>\d+)/$', 
        'django.views.generic.list_detail.object_detail',
        {'queryset':Meeting.objects.all()}),

    (r'^location/(?P<object_id>\d+)/$', 
        'django.views.generic.list_detail.object_detail', 
        {'queryset':Location.objects.all()}),
    
    (r'^speaker/(?P<object_id>\d+)/$', 
        'django.views.generic.list_detail.object_detail', 
        {'queryset':Speaker.objects.all()}),

    (r'^image/(?P<path>.+)/$', 
        'meetings.views.view_image'),

    (r'^admin/', include('django.contrib.admin.urls')),

    (r'^feeds/(?P<url>.*)/$', 
        'django.contrib.syndication.views.feed', 
        {'feed_dict': feeds}),
)
