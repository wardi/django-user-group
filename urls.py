from django.conf.urls.defaults import *

from meetings.models import Meeting, Location, Speaker, Announcement
from meetings.feeds import UpcomingMeetings

import datetime

def now_plus_meeting_length():
    return datetime.datetime.now() + datetime.timedelta(hours=2)


upcoming_meetings = {
    'queryset': Meeting.objects.filter(visible=True,
        date__gte=now_plus_meeting_length).order_by("date"),
    'template_name': 'meetings/upcoming.html',
    'allow_empty': True,
    'extra_context': {
        'announcements':
            lambda: Announcement.objects.filter(visible=True)
    }
}

past_meetings = {
    'queryset': Meeting.objects.filter(visible=True,
        date__lt=now_plus_meeting_length),
    'template_name': 'meetings/past.html',
    'allow_empty': True,
    'paginate_by': 20,
}

feeds = {
    'upcoming': UpcomingMeetings,
}

urlpatterns = patterns('',
    (r'^$', 
        'django.views.generic.list_detail.object_list', 
        upcoming_meetings),
        
    (r'^past_meetings/$', 
        'django.views.generic.list_detail.object_list',
        past_meetings),

    (r'^meeting/(?P<object_id>\d+)/$', 
        'django.views.generic.list_detail.object_detail',
        {'queryset':Meeting.objects.filter(visible=True)}),

    (r'^location/(?P<object_id>\d+)/$', 
        'django.views.generic.list_detail.object_detail', 
        {'queryset':Location.objects.all()}),
    
    (r'^speaker/(?P<object_id>\d+)/$', 
        'django.views.generic.list_detail.object_detail', 
        {'queryset':Speaker.objects.all()}),

    (r'^admin/', include('django.contrib.admin.urls')),

    (r'^feeds/(?P<url>.*)/$', 
        'django.contrib.syndication.views.feed', 
        {'feed_dict': feeds}),
)
