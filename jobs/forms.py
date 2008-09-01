from django.forms import ModelForm
from models import Posting

class PostingForm(ModelForm):
    class Meta:
        model = Posting
        # Don't alllow user to edit date fields in this model
        exclude = ['created', 'expires', 'accepted']

