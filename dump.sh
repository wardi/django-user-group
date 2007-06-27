#!/bin/sh

# Dump the tables used by the django contrib apps and 
# our own custom "meetings" app into an xml format
# (not quite as unpleasant as "--format json" or "--format python")

# Don't include the "auth" tables so that we don't distribute
# private info and password hashes.

# Don't include the "sessions" tables because that would allow
# session hijacking (and they're boring)

python manage.py dumpdata --format xml --indent 4 \
    sites flatpages redirects meetings

#    > /home/webdude/site_data/db.xml
