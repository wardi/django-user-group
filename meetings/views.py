# Create your views here.

from django.views.generic.list_detail import object_detail, object_list
from django.shortcuts import get_object_or_404, render_to_response

from models import Image, Meeting, Location, Speaker, Announcement, File

import datetime

# show meetings that have not yet finished on the upcoming page
# and the rest on the past meetings page.  A meeting is considered
# "done" 2 hours after it starts.

def now_less_meeting_length():
    return datetime.datetime.now() - datetime.timedelta(hours=2)


recent_meetings = Meeting.objects.filter(visible=True,
    date__lt=now_less_meeting_length).order_by("-date")

def upcoming_meetings(request, template_name='meetings/upcoming.html',
    extra_content={}):
    """
    This is the front page of the site.  Use the generic view object_list
    to display the list of upcoming meetings.  Also display the most
    recently passed meeting.
    
    Extra box content from other applications (eg. feedjack) is passed 
    in as extra_content by urls.py
    """ 
    return object_list(request, 
        queryset=Meeting.objects.filter(visible=True,
            date__gte=now_less_meeting_length).order_by("date"),
        template_name=template_name,
        allow_empty=True,
        extra_context=dict(extra_content,
            announcements=lambda: Announcement.objects.filter(visible=True),
            recent=lambda: recent_meetings[:1]))

def past_meetings(request, template_name='meetings/past.html', 
    extra_content={}):
    """
    Display a text list of 20 meetings on the right with full details of
    the most recent 5 meetings on the left.  The template will hide
    the most recent 5 when the earlier meetings are displayed from the
    text list.
    """
    return object_list(request, 
        queryset= Meeting.objects.filter(visible=True,
            date__lt=now_less_meeting_length),
        template_name=template_name,
        allow_empty=True,
        paginate_by=20,
        extra_context=dict(extra_content,
            recent=lambda: recent_meetings[:5]))


def view_image(request, path, template_name="meetings/image_detail.html"):
    """
    Wrap images in a simple template.
    """
    img = get_object_or_404(Image, src=path)
    return render_to_response(template_name, {'img':img})


def list_files(request, template_name="meetings/files.html"):
    """
    Display a text list of files that may be downloaded.
    """
    return object_list(request, 
        queryset=File.objects.order_by('label'),
        template_name=template_name,
        allow_empty=True,
        paginate_by=50)


# The following are wrappers around the generic view object_detail
# added just to be explicit about the templates that will be used
# and to remove some clutter from url.py 

def meeting_detail(request, object_id, 
    template_name="meetings/meeting_detail.html"):
    return object_detail(request, object_id=object_id, 
        template_name=template_name, queryset=Meeting.objects.all())

def location_detail(request, object_id,
    template_name="meetings/location_detail.html"):
    return object_detail(request, object_id=object_id, 
        template_name=template_name, queryset=Location.objects.all())

def speaker_detail(request, object_id,
    template_name="meetings/speaker_detail.html"):
    return object_detail(request, object_id=object_id, 
        template_name=template_name, queryset=Speaker.objects.all())
