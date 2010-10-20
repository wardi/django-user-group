OCLUG Django Site Code
----------------------

This is a copy of the code running the Ottawa Canada Linux Users Group
web site.  It hosts meeting announcements, job postings and embeds an
external RSS feed.

This code is being retired for OCLUG, but may be useful for other groups that
want a meeting announcement site that is simple and keeps the front page
current.


Required Software
=================

For development of the OCLUG web site you will need the following:


 * Apache 2.x with mod_python
 * Python, python-markdown and python-imaging
 * Subversion
 * Sqlite (or PostgreSQL or MySQL if you prefer)
 * `Django <http://www.djangoproject.com/>`_ >= 1.0

Everything except Django can be installed on Debian or Ubuntu systems with this command run as root (or with ``sudo``)::

    sudo apt-get install apache2 libapache2-mod-python subversion \
    python python-markdown python-imaging python-pysqlite2


or on Ret Hat/Fedora systems you will first have to download python-markdown by following the link from http://www.freewisdom.org/projects/python-markdown/ then do the following::

  cd python-markdown-*
  python setup.py install
  yum install httpd mod_python subversion python python-imaging python-sqlite


Install Django by downloading the latest 1.1 tarball from the 
`Django download page <http://www.djangoproject.com/download/>`_, or
if you are running Debian or Ubuntu you can install the packaged
version with::

  apt-get install python-django

As of October 2010 the latest 1.1 version of Django is 1.1.2.  The following commands will download and install this version::

  wget http://www.djangoproject.com/download/1.1.2/tarball/
  tar xzvf Django-1.1.2-final.tar.gz
  cd Django-1.1.2-final/
  sudo python setup.py install --prefix=/usr/local


You can verify your installation by running::

  python -c 'import django; print django.VERSION'

It should print something like ``(1, 1, 2, 'final', 0)``.


Setting up the Working Directory
================================


These instructions suggest installing the code in a regular user account's home direcory.  

Make sure the user account's home directory is accessible by apache by running::

  ls -ald $HOME


If the set of characters printed starting with `drwx` ends with a `-` instead of an `x` 
then you need to change the default permissions.  
If you do not want to make your home directory world-traversable 
you may want to create a separate user account at this time.  
This command will make the home directory world-traversable::

  chmod a+x $HOME


Downloading the Code and Site data
==================================

.. NOTE::
   These instructions will stop working once the devel.oclug.on.ca site
   is taken offline.

Run these commands starting from your home directory to create an 
``oclug_site`` directory 

and download the OCLUG site code and data::

  cd
  mkdir oclug_site
  cd oclug_site
  svn co http://devel.oclug.on.ca/svn/oclug_django_site/trunk oclug_django_site
  svn co http://devel.oclug.on.ca/svn/site_data/trunk site_data


Site Configuration
==================

You will need to create a settings file called ``local_settings.py`` in your 
``oclug_django_site`` directory::

  cd $HOME/oclug_site/oclug_django_site
  sed "s/PUT-RANDOM-STUFF-HERE/$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM$RANDOM/;
  s{USERS-HOME-DIRECTORY{$HOME{;" < local_settings.sample.py > local_settings.py

Next set up a database and a writable directory for Apache::

  sudo mkdir -p /var/local/apache_writable/oclug_uploaded/
  sudo cp -r $HOME/oclug_site/site_data/uploaded/* /var/local/apache_writable/oclug_uploaded/
  cd $HOME/oclug_site/oclug_django_site
  sudo python manage.py syncdb  # this will let you create an admin account
  sudo python manage.py loaddata $HOME/oclug_site/site_data/db.xml
  sudo chown -R www-data: /var/local/apache_writable/  # use "apache" instead of www-data on Red Hat systems


The account you created will be used to access the ``/admin/`` pages on the web site.

We also need to create two symlinks to allow Apache to find some of the media files.
The first one lets Apache find the uploaded files in the directory writable by
Apache, which we created above.  The second allows the admin site to be displayed
with all its images and formatting::

  ln -s /var/local/apache_writable/oclug_uploaded/ $HOME/oclug_site/uploaded
  ln -s `python -c'import django, os; print os.path.dirname(django.__file__)'`/contrib/admin/media/ \
  $HOME/oclug_site/admin


Apache Configuration
====================



General apache configuration is covered in `How to use Django with mod_python <http://docs.djangoproject.com/en/1.1/howto/deployment/modpython/>`_.

If your apache is configured to use virtual hosts with a `NameVirtualHost *`
directive then your configuration for the
OCLUG Django site would look something like::

  <VirtualHost * >
      DocumentRoot /home/(MY-USER-NAME)/oclug_site/oclug_django_site/docroot
      
      <Location "/">
          SetHandler python-program
          PythonHandler django.core.handlers.modpython
          SetEnv DJANGO_SETTINGS_MODULE settings
          PythonPath "['/home/(MY-USER-NAME)/oclug_site/oclug_django_site/'] + sys.path"
          PythonDebug Off
      </Location>
  
      <Location "/images/">
          SetHandler None
      </Location>
      <Location "/media/">
          SetHandler None
      </Location>
      <Location "/favicon.ico">
          SetHandler None
      </Location>
  </VirtualHost>


The ``/images/``, ``/media/`` and ``/favicon.ico`` location blocks allow
images and files to be served by Apache.
All other URLs are handled by the Django site.

Restart apache and browse to `http://localhost/` to see if everything worked.  
You can browse to `http://localhost/admin/` to use the site administration interface
with the account created above.



Updating Your Copy
==================

.. NOTE::
   These instructions will stop working once the devel.oclug.on.ca site
   is taken offline.

You can use `svn update` to update your `oclug_django_site` directory.

To update your `site_data` and reset your local copy of the database, use these
commands::

  cd oclug_site/site_data
  svn update
  sudo cp -r $HOME/oclug_site/site_data/uploaded/* /var/local/apache_writable/oclug_uploaded/
  cd ../oclug_django_site
  sudo python manage.py loaddata ../site_data/db.xml

