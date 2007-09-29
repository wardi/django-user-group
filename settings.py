# Django settings for oclug_django_site project.

from local_settings import DEBUG, DATABASE_ENGINE, DATABASE_NAME, \
    DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, \
    SECRET_KEY, MEDIA_ROOT, TEMPLATE_DIRS

# The settings above were removed from this file so that they can be 
# customized on a per-site basis.  local_settings.py is not checked in
# with the rest of the source code, if you are running this code on
# a different system create a local_settings.py file with content like
# the following:
#
## # Example local_settings.py
##
## DEBUG = True
##
## DATABASE_ENGINE = 'sqlite3'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
## DATABASE_NAME = '/var/local/apache_writable/oclug.db'     # Or path to database file if using sqlite3.
## DATABASE_USER = ''             # Not used with sqlite3.
## DATABASE_PASSWORD = ''         # Not used with sqlite3.
## DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
## DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.
##
## 
## # Make this unique, and don't share it with anybody.
## SECRET_KEY = '(t$6(biz=dc*ecq%2*p$uwsog9y*r-#i_vx#iom=5x*2fp2vr)'
##
## # Absolute path to the directory that holds media.
## # Example: "/home/media/media.lawrence.com/"
##
## MEDIA_ROOT = '/var/local/apache_writable/oclug_uploads/'
## TEMPLATE_DIRS = (
##     # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
##     # Always use forward slashes, even on Windows.
##     # Don't forget to use absolute paths, not relative paths.
##     '(PLACE-WHERE-WHERE-YOU-HAVE-oclug_django_site)/templates',
## )
#
#
# If you use the settings above you will need to set up the "apache_writable"
# directory.  To set up the directory and load the site data run the following
# as root:
#
## mkdir -p /var/local/apache_writable/oclug_uploaded/
## rsync -r --exclude .svn (PLACE-WHERE-YOU-HAVE-site_data)/uploaded/ /var/local/apache_writable/oclug_uploaded/
## cd (PLACE-WHERE-WHERE-YOU-HAVE-oclug_django_site)
## python manage.py syncdb  # this will let you create an admin account
## python manage.py loaddata (PLACE-WHERE-YOU-HAVE-site_data)/db.xml
## chown -R www-data: /var/local/apache_writable/


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
