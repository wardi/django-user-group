from django.utils.html import escape
from django.template import Library

register = Library()

def meetings_image(obj, extra=""):
    """
    Generate a complete <img> tag based on the image model "obj".
    "extra" may contain extra attributes for the <img>.
    """
    
    if extra:
        extra = " "+extra
    return '<img src="%s" alt="%s" title="%s" width="%d" height="%d"%s/>' %(
        obj.get_src_url(), escape(obj.alt), escape(obj.title),
        obj.width, obj.height, extra)
meetings_image = register.simple_tag(meetings_image)
        
