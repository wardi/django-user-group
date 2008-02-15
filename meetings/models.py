from django.db import models

import datetime


class Image(models.Model):
    reuse = models.BooleanField(default=False,
        help_text='Check if you expect to reuse this image for different '
        'talks, meetings etc.')
    title = models.CharField(max_length=100,
        help_text='Text that appears when the user hovers their cursor '
        'over the image')
    alt = models.CharField(max_length=100,
        help_text='Text that appears when the image cannot be rendered')
    src = models.ImageField(upload_to='%Y/%m/%d',
        height_field='height', width_field='width')
    width = models.IntegerField(editable=False)
    height = models.IntegerField(editable=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.get_src_url()

    class Admin:
        list_display = ['get_src_url','title','alt','reuse', 'width', 'height']
        list_filter = ['reuse']
        search_fields = ['title','alt']
        
    class Meta:
        ordering = ['src']


class Announcement(models.Model):
    visible = models.BooleanField(default=True,
        help_text = 'Whether this announcement is visible on the '
        'front page')
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200,
        help_text='The title of the announcement, '
        'eg. "OCLUG Sponsors Algonquin Programming Olympics"')
    text = models.TextField(
        help_text='The announcement text to appear on the front page')
    image = models.ForeignKey(Image, null=True, blank=True, 
        help_text='An Image to display with the announcement')
    
    def __str__(self):
        return self.title

    class Admin:
        list_display = ['title','visible']
        list_filter = ['visible']
        search_fields = ['title','text']
        save_on_top = True

    class Meta:
        ordering = ['created']


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True,
        help_text='A brief description of the location,  '
        'eg. "Algonquin College (Woodroffe Campus), room C144"')
    directions = models.TextField(blank=True,
        help_text='Detailed diretions to the loctaion,  '
        'eg. "Algonquin College is close to the corner of '
        'Woodroffe and Baseline and right across from the '
        'Baseline transitway station.  Room C114 is in '
        'Building C in the south-west corner of the campus. '
        'Free parking is available in lots 8, 9 and 12 '
        'after 5pm.", in "Markdown" format')
    url = models.CharField(max_length=300, blank=True,
        help_text='A URL showing the location in the city, '
        'eg. "http://maps.google.com/maps?q=Algonquin+College'
        '-Woodroffe,+Canada"')
    detail_url = models.CharField(max_length=300, blank=True,
        help_text='A URL showing a more detailed view of the '
        'location, eg. http://www.algonquincollege.com/main/'
        'yourAlgonquinTab/directions/woodroffeMap.htm"')
    active = models.BooleanField(default=True,
        help_text='Whether this location should be shown when '
        'choosing the location of a new meeting.')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/location/%d/" % self.id

    class Admin:
        list_display = ['name','active']
        list_filter = ['active']
        search_fields = ['name','directions']
        
    class Meta:
        ordering = ['name']


def next_meeting():
    try:
        prev = Meeting.objects.latest().date
    except Meeting.DoesNotExist:
        prev = datetime.datetime.now()
    next_yr, next_mn = prev.year, prev.month+1
    if next_mn==13:
        next_yr, next_mn = next_yr+1, 1
    next = datetime.datetime(next_yr, next_mn, 1, 19)
    wd = next.weekday() # 0 = Monday
    # shift to the first Tuesday
    return next + datetime.timedelta([1, 0, 6, 5, 4, 3, 2][wd])

MEETING_FORMATS = [
    ('A', 'AGM'), 
    ('M', 'Meeting'), 
    ('T', 'Tutorial'),
    ('W', 'LITW')]

class Meeting(models.Model):
    summary = models.CharField(max_length=200,
        help_text='A summary of the meeting topics, '
        'eg. "Linux on laptops lighting talks"')
    description = models.TextField(blank=True,
        help_text='A description of events at the meeting '
        'not described in the talk descriptions, in "Markdown" '
        'format')
    format = models.CharField(max_length=1, default='M',
        choices=MEETING_FORMATS)
    date = models.DateTimeField(default=next_meeting)
    location = models.ForeignKey(Location, related_name='meetings',
        limit_choices_to={'active':True},)
    visible = models.BooleanField(default=False)
    image = models.ForeignKey(Image, null=True, blank=True, 
        help_text='Image to be displayed next to the meeting '
        'information')
    donations = models.DecimalField(max_digits=10, decimal_places=2,
        null=True, blank=True,
        help_text='Amount donated at this meeting')
    
    def __str__(self):
        return self.summary
   
    def readable_format(self, hide_year=False):
        """
        return a string describing the meeting format.

        hide_year -- if True then the year will be hidden for LITW and AGMs
        """

        if self.format == "A":
            return self.date.strftime("%Y ") * (not hide_year) + "AGM"
        if self.format == "W":
            return self.date.strftime("%Y ") * (not hide_year) + "LITW"
        mn = self.date.strftime("%B")
        if self.format == "M":
            return mn + " Meeting"
        if self.format == "T":
            return mn + " Tutorial"
    
    def readable_format_no_year(self):
        """a convenience function for calling from templates"""
        return self.readable_format(hide_year=True)

    def get_absolute_url(self):
        return "/meeting/%d/" % self.id
    
    class Admin:
        list_display = ['summary','format','date','visible',
            'location']
        date_hierarchy = 'date'
        list_filter = ['format']
        search_fields = ['summary', 'description', 'talks__topic', 
            'talks__description']
        fields = [
            (None, {'fields': [['visible', 'summary'], 
                ['format', 'location'],
                'date']}),
            ('Extra Description', {'fields': ['description', 'image'],
                'classes': 'collapse'}),
            ('Accounting', {'fields': ['donations'],
                'classes': 'collapse'})]
        save_on_top = True
    
    class Meta:
        ordering = ['-date']    
        get_latest_by = 'date'


class Speaker(models.Model):
    name = models.CharField(max_length=50, unique=True,
        help_text='The full name of the speaker')
    background = models.TextField(blank=True,
        help_text="The speaker's background (if available), "
            'Written in "Markdown" format')
    image = models.ForeignKey(Image, null=True, blank=True, 
        help_text='Picture of the speaker')

    def get_absolute_url(self):
        return "/speaker/%d/" % self.id

    def __str__(self):
        return self.name

    class Admin:
        search_fields = ['name', 'background']

    class Meta:
        ordering = ['name']
    

class Talk(models.Model):
    topic = models.CharField(max_length=100, core=True,
        help_text='A one-line description of the talk being given')
    description = models.TextField(blank=True,
        help_text='A full summary of the talk, in "Markdown" format')
    meeting = models.ForeignKey(Meeting, related_name='talks',
        edit_inline=models.STACKED, num_in_admin=2)
    speaker = models.ForeignKey(Speaker, related_name='talks')
    image = models.ForeignKey(Image, null=True, blank=True, 
        help_text='Image to be displayed next to the talk description')
        
    def __str__(self):
        return self.topic
    
    ## don't show on the admin interface, these should be edited from
    ## the Meeting page
    #
    #class Admin:
    #    search_fields = ['topic', 'description']
    #    list_display = ['topic', 'meeting', 'speaker']
        
    class Meta:
        ordering = ['topic']
        order_with_respect_to = 'meeting'


class File(models.Model):
    label = models.CharField(max_length=200,
        help_text='A brief description of the file')
    file = models.FileField(upload_to='%Y/%m/%d')

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return self.get_file_url()

    class Admin:
        list_display = ['label','get_file_url', 'get_file_size']
        search_fields = ['label']
        
    class Meta:
        ordering = ['label']
