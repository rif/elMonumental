# -*- coding: utf-8 -*-
# Django settings for elMonumental project.
import os
def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

MANAGERS = ADMINS = (
    ('Radu Ioan Fericean', 'radu.fericean@oce.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':  rel('database.sqlite')
    }
}

TIME_ZONE = 'Europe/Bucharest'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = True
EMAIL_HOST = 'smtp.oce.net'
EMAIL_PORT = '25'
EMAIL_SUBJECT_PREFIX = ' [elMonumental] '
ACCOUNT_ACTIVATION_DAYS = 7

#CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = rel('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

LOGOUT_URL = '/'
LOGIN_REDIRECT_URL = '/'
AUTH_PROFILE_MODULE = 'scheduler.PlayerProfile'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'k62tqz=o-^$vh1^$uf_6xzkutj-qczsk2usgn2as&c#$6m$v#g'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
)

if DEBUG:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'elMonumental.urls'

TEMPLATE_DIRS = (
    rel('templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.comments',
    'django.contrib.markup',
    # Third party apps
    'forum',
    'south',
    'registration',
    'profiles',
    # My apps
    'scheduler',
    'news',
)

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)

FORUM_BASE = '/forum'

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'HIDE_DJANGO_SQL': True,
}
INTERNAL_IPS = ('127.0.0.1',)
