# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

# Django settings for dolweb project.
# -*- encoding: utf-8 -*-

import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SERVE_MEDIA = DEBUG

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

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
    ('ast', 'Asturianu'),
    ('ms', 'Bahasa Melayu'),
    ('ca', 'Català'),
    ('cs', 'Česky'),
    ('cy', 'Cymraeg'),
    ('da', 'Dansk'),
    ('de', 'Deutsch'),
    ('en', 'English'),
    ('es', 'Español'),
    ('el', 'Ελληνικά'),
    ('fr', 'Français'),
    ('gl', 'Galego'),
    ('it', 'Italiano'),
    ('hu', 'Magyar'),
    ('nl', 'Nederlands'),
    ('nb', 'Norsk (Bokmål)'),
    ('pl', 'Polski'),
    ('pt', 'Português'),
    ('br', 'Português (Brasil)'),
    ('ru', 'Русский'),
    ('sv', 'Svenska'),
    ('tr', 'Türkçe'),
    ('cn', '中文(中国)'),
    ('ja', '日本語'),
    ('ko', '한국어'),
)

# Languages that are read from right to left.
RTL_LANGUAGES = (
    'fa',
)

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

SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'dolweb', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dolweb.utils.context_processors.website_urls',
                'dolweb.utils.context_processors.guess_system_from_ua',
                'dolweb.utils.context_processors.check_country_redirect',
                'dolweb.utils.context_processors.export_languages',
            ],
        },
    },
]

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
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
    'dolweb.update',
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
ISSUES_URL = "https://bugs.dolphin-emu.org/projects/emulator/issues"
UPDATE_MANIFEST_URL = "https://update.dolphin-emu.org/manifest/%s/%s/%s/%s.manifest"

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
ZINNIA_MAIL_COMMENT_AUTHORS = False
ZINNIA_ENTRY_BASE_MODEL = 'dolweb.blog.models.BlogEntry'
ZINNIA_FEEDS_FORMAT = 'atom'
ZINNIA_FEEDS_MAX_ITEMS = 20
ZINNIA_PROTOCOL = 'https'

from markdown.extensions.toc import TocExtension
ZINNIA_MARKUP_LANGUAGE = 'markdown'
ZINNIA_MARKDOWN_EXTENSIONS = [
    TocExtension(permalink=True),
    'markdown.extensions.tables',
]

BLOG_ETHERPAD_URL = ''
BLOG_ETHERPAD_API_KEY = ''
BLOG_ETHERPAD_HMAC_KEY = ''

# Whitelist for the management interface.
#
# WARNING: This management interface gives shell access on the web server. TAKE
# IT SERIOUSLY and do not let untrusted users in the whitelist.
#
# This variable is a list of ('username', 'password').
MGMT_AUTHORIZED_USERS = []

# Names of the automatically maintained auto-update tracks and what branch they
# follow.
AUTO_MAINTAINED_UPDATE_TRACKS = {
    'dev': 'master',
}

# URL of the update content store.
UPDATE_CONTENT_STORE_URL = 'https://update.dolphin-emu.org/content/'

local_settings_file = os.path.join(PROJECT_ROOT, 'dolweb', 'local_settings.py')
if os.path.exists(local_settings_file):
    local = compile(
        open(local_settings_file).read(), local_settings_file, 'exec')
    exec(local, globals(), locals())
