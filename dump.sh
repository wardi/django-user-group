#!/bin/sh

./manage.py dumpdata --format xml --indent 4 sites flatpages redirects meetings > meetings/fixtures/initial_data.xml
