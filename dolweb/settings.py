# Django settings for dolweb project.
# -*- encoding: utf-8 -*-

import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SERVE_MEDIA = DEBUG

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ['.dolphin-emu.org']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
    'wiki': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
}

DATABASE_ROUTERS = (
    'dolweb.utils.db.WikiRouter',
)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# List of supported languages: ('langcode', 'Name of the language')
LANGUAGES = (
    ('ast', u'Asturianu'),
    ('ms', u'Bahasa Melayu'),
    ('ca', u'Català'),
    ('cs', u'Česky'),
    ('cy', u'Cymraeg'),
    ('de', u'Deutsch'),
    ('en', u'English'),
    ('es', u'Español'),
    ('el', u'Ελληνικά'),
    ('fr', u'Français'),
    ('it', u'Italiano'),
    ('hr', u'Hrvatski'),
    ('hu', u'Magyar'),
    ('nl', u'Nederlands'),
    ('pl', u'Polski'),
    ('pt', u'Português'),
    ('br', u'Português (Brasil)'),
    ('ru', u'Русский'),
    ('sv', u'Svenska'),
    ('tr', u'Türkçe'),
    ('cn', u'中文(中国)'),
    ('ja', u'日本語'),
    ('ko', u'한국어'),
    ('fa', u'ﻑﺍﺮﺳی'),
)

# Languages that are read from right to left.
RTL_LANGUAGES = (
    'fa',
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media', 'user')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '//dolphin-emu.org/m/user/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'media', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '//dolphin-emu.org/m/static/'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'dolweb', 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '#-$yw(*dcl050c6(6v#lz1qa)$f^u001ehe44n@uq_&amp;1%73dnu'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'sslify.middleware.SSLifyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'dolweb.utils.country_redirect.CountryRedirectMiddleware',
    # Uncomment the next line for simple clickjacking protection:
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'dolweb.utils.context_processors.website_urls',
    'dolweb.utils.context_processors.guess_system_from_ua',
    'dolweb.utils.context_processors.check_country_redirect',
)

ROOT_URLCONF = 'dolweb.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'dolweb.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'dolweb', 'templates'),
)

LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, 'dolweb', 'locale'),
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'dolphin-emu-www',
    },
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',

    # External
    'bootstrapform',
    'debug_toolbar',
    'sorl.thumbnail',
    'markup_deprecated',
    # Blog dependencies
    'django_comments',
    'tagging',
    'mptt',

    # Internal
    'dolweb.homepage',
    'dolweb.downloads',
    'dolweb.docs',
    'dolweb.management',
    'dolweb.media',
    'dolweb.compat',
    'dolweb.localefixes',
    # External blog, after 'dolweb.blog' for template overwriting
    'dolweb.blog',
    'zinnia',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
    },
    'loggers': {
        'django.request': {
            'handlers': [],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Links and templates for links to other Dolphin properties.
FORUM_URL = "https://forums.dolphin-emu.org/"
WIKI_URL = "https://wiki.dolphin-emu.org/"
GIT_AUTHOR_URL = "https://github.com/%s"
GIT_BROWSE_URL = "https://github.com/dolphin-emu/dolphin"
GIT_CLONE_URL = "https://github.com/dolphin-emu/dolphin.git"
GIT_COMMIT_URL = "https://github.com/dolphin-emu/dolphin/commit/"
GIT_PR_URL = "https://github.com/dolphin-emu/dolphin/pull/%s"
WEBSITE_GIT_URL = "https://github.com/dolphin-emu/www"
ISSUES_URL = "https://bugs.dolphin-emu.org/projects/redmine/issues"

# Used for i18n purposes: the language code is prepended to this default
# hostname.
DEFAULT_HOST = "dolphin-emu.org"

# Should the access to the wiki database be read-only. In production, you DO
# want this enabled since otherwise syncdb might kill the wiki database. In
# testing, you want to disable this so that syncdb installs a schema on your
# testing database.
WIKI_DB_READ_ONLY = True

# Name of the DATABASES entry that contains Wiki tables (page, revision, ...).
# In production, this has to be the Mediawiki database. In testing, this should
# be the default database, which is where the tables are syncdb'd.
WIKI_DB_NAME = 'wiki'

# Google analytics account ID, or '' to disable GA tracking.
GOOGLE_ANALYTICS_ACCOUNT = ''

# Social media links information.
FB_LIKE_PAGE = 'http://www.facebook.com/dolphin.emu'
GPLUS_LIKE_PAGE = 'http://dolphin-emu.org/'

# Not directly used by the website, but used by one of the management commands
# (genatlas) that reads banner from MongoDB and turns it into image atlases.
BNR_MONGO_HOST = ''
BNR_MONGO_DBNAME = ''
BNR_MONGO_USER = ''
BNR_MONGO_PASSWORD = ''

# Path used to load and update dynamic i18n PO files
DYNI18N_PATH = os.path.join(PROJECT_ROOT, 'dyni18n')

# Transifex informations for automatic dyni18n pull
TRANSIFEX_USER = ''
TRANSIFEX_PASSWORD = ''
TRANSIFEX_PROJECT = ''
TRANSIFEX_FAQ_RESOURCE = ''

# Blog settings
HOMEPAGE_ARTICLES = 3
FORUM_URL_FOR_THREAD = 'https://forums.dolphin-emu.org/showthread.php?tid={id}'
ZINNIA_MARKUP_LANGUAGE = 'markdown'
ZINNIA_MAIL_COMMENT_AUTHORS = False
ZINNIA_ENTRY_BASE_MODEL = 'dolweb.blog.models.BlogEntry'
ZINNIA_FEEDS_FORMAT = 'atom'
ZINNIA_FEEDS_MAX_ITEMS = 20
ZINNIA_PROTOCOL = 'https'

# Whitelist for the management interface.
#
# WARNING: This management interface gives shell access on the web server. TAKE
# IT SERIOUSLY and do not let untrusted users in the whitelist.
#
# This variable is a list of ('username', 'password').
MGMT_AUTHORIZED_USERS = []

local_settings_file = os.path.join(PROJECT_ROOT, 'dolweb', 'local_settings.py')
if os.path.exists(local_settings_file):
    try:
        execfile(os.path.join(local_settings_file), globals(), locals())
    except IOError, ImportError:
        print 'Warning: could not import dolweb.local_settings'
