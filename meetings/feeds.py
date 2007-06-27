from django.contrib.syndication.feeds import Feed
from models import Meeting

import datetime


class UpcomingMeetings(Feed):
    title = "OCLUG Upcoming Meetings"
    link = "/"
    description = "Upcoming meetings and events for the "\
        "Ottawa Canada Linux Users Group"

    def items(self):
        return Meeting.objects.filter(visible=True,
            date__gte=datetime.datetime.now).order_by('date')[:10]

