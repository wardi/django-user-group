# Django settings for oclug_django_site project.

from local_settings import DEBUG, DATABASE_ENGINE, DATABASE_NAME, \
    DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, \
    SECRET_KEY, MEDIA_ROOT, TEMPLATE_DIRS

# The settings above were removed from this file so that they can be 
# customized on a per-site basis.  local_settings.py is not checked in
# with the rest of the source code, if you are running this code on
# a different system create a local_settings.py file with content like
# what is found in local_settings.sample.py


TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('OCLUG Web List', 'oclug-www@lists.oclug.on.ca'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Toronto'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/media/uploaded/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.markup',
    'django.contrib.flatpages',
    'django.contrib.redirects',
    'meetings',
)

try:
    import feedjack
    INSTALLED_APPS = INSTALLED_APPS + ('feedjack',)
except ImportError, err:
    # ignore a nonexistant feedjack (not required for remote development)
    pass


# use local-memory caching backend
CACHE_BACKEND = 'locmem:///'

# be sure to append slashes (done by CommonMiddleware)
APPEND_SLASH = True
