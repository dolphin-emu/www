Contributing to the Dolphin website
===================================

First of all, we gladly accept contributions to this website! Before starting
anything, you might want to come on IRC (#dolphin-dev @ irc.freenode.net) and
discuss with ``delroth`` (main website developer) about your idea. The website
is a critical piece of our infrastructure since it is what allows people to
download and find documentation about our application, so we take changes
seriously and try to maintain a good quality.

A file called ``TODO`` at the root of this repository gives a few ideas of tasks
we know are needed. They are not necessarily easy, but worth trying to tackle if
you're lacking ideas and want to help.

Use of Git
----------

The Git branch deployed on the main website instance (https://dolphin-emu.org/)
is the ``stable`` branch. When we do large scale changes that require staging
and more testing, we work in the ``master`` branch, which is deployed on a
special website instance (https://dev.dolphin-emu.org/). Note that these two
website instances share their database - as such, database schema changes
require more involved staging.

Running a testing instance locally
----------------------------------

First of all, create a Python 3.6+ virtual environment and make sure you
are in it (``echo $VIRTUAL_ENV``). Then install all the required dependencies
with ``pip``:

    pip install -r requirements.txt

Set up a local configuration by creating a ``local_settings.py`` file next to
the ``settings.py`` file (in the ``dolweb/`` directory):

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'dolweb.db',
        },
    }

    WIKI_DB_NAME = 'default'

    MEDIA_URL = '/m/user/'
    STATIC_URL = '/m/static/'

Remove the redirection to HTTPS and allow localhost by modifying
``dolweb/settings.py``:

    SECURE_SSL_REDIRECT = False

    ALLOWED_HOSTS = ['localhost']

Then run ``migrate`` to create a default database.

    python manage.py migrate

Then run a local web server, and browse to http://localhost:8000/ :

    python manage.py runserver

This should be enough to get started on most changes. The admin can be accessed
(as usual on Django applications) at http://localhost:8000/admin/ .
