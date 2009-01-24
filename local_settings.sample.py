# Example local_settings.py
##
DEBUG = True
##
DATABASE_ENGINE = 'sqlite3'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = '/var/local/apache_writable/oclug.db'     # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.
##

# where error emails will be sent
ADMINS = (
#    ('Admin Person', 'admin@person.somewhere'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'PUT-RANDOM-STUFF-HERE'
##
# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
##
MEDIA_ROOT = '/var/local/apache_writable/oclug_uploaded/'
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'USERS-HOME-DIRECTORY/oclug_site/oclug_django_site/templates',
)

# Jobs application email addresses
# not required unless your are testing notification of new job postings
#
#JOB_POSTING_EMAILS = ['person1@somehost1', 'person2@somehost2']
#JOB_POSTING_FROM = 'jobs@thisdjangosite'

