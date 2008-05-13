# Django settings for feedjack rss aggregation sites.

from settings import *

from django.conf.urls.defaults import patterns, include

assert 'feedjack' in INSTALLED_APPS, "Failed to locate feedjack module, is it installed properly?"

MEDIA_URL = '/static/'
ROOT_URLCONF = 'feedjack_settings' # look at this module for URLs (see below)

urlpatterns = patterns('', (r'', include('feedjack.urls')))
