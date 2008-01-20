# Create your views here.

from django.views.generic.list_detail import object_detail
from django.shortcuts import get_object_or_404, render_to_response

from models import Image

def view_image(request, path):
    img = get_object_or_404(Image, src="/media/uploaded/"+path)
    return render_to_response('meetings/image_detail.html', {'img':img})
