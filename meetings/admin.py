from django.contrib import admin
from models import Image, Announcement, Location, Meeting, Speaker, File, Talk


class ImageAdmin(admin.ModelAdmin):
    list_display = ['get_absolute_url','title','alt','reuse', 'width', 'height']
    list_filter = ['reuse']
    search_fields = ['title','alt']
admin.site.register(Image, ImageAdmin)
    
    
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title','visible']
    list_filter = ['visible']
    search_fields = ['title','text']
    save_on_top = True
admin.site.register(Announcement, AnnouncementAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = ['name','active']
    list_filter = ['active']
    search_fields = ['name','directions']
admin.site.register(Location, LocationAdmin)


class TalkInline(admin.StackedInline):
    model = Talk
    max_num = 3


class MeetingAdmin(admin.ModelAdmin):
    list_display = ['summary','format','date','visible',
        'location']
    date_hierarchy = 'date'
    list_filter = ['format']
    search_fields = ['summary', 'description', 'talks__topic', 
        'talks__description']
    fieldsets = (
        (None, {'fields': (('visible', 'summary'), 
            ('format', 'location'),
            'date')}),
        ('Extra Description', {'fields': ('description', 'image')}),
        ('Accounting', {'fields': ('donations',),
            'classes': ('collapse',)}))
    save_on_top = True
    inlines = [TalkInline]
admin.site.register(Meeting, MeetingAdmin)


class SpeakerAdmin(admin.ModelAdmin):
    search_fields = ['name', 'background']
admin.site.register(Speaker, SpeakerAdmin)


class FileAdmin(admin.ModelAdmin):
    list_display = ['label','get_absolute_url']#, 'get_file_size']  Django bug 8466
    search_fields = ['label']

admin.site.register(File, FileAdmin)    


