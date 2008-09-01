from django.contrib import admin
from models import Posting


class PostingAdmin(admin.ModelAdmin):
    list_display = ['title', 'visible', 'created', 'accepted']
    search_fields = ['title', 'description', 'contact']
    save_on_top = True
    ordering = ['accepted']
admin.site.register(Posting, PostingAdmin)
    
    

