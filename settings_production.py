from settings_development import *

DEBUG = TEMPLATE_DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'elMonumental',
        'USER': 'elAdmin',
        'PASSWORD': 'testus_cumulus',
        'HOST': '',
        'PORT': '',
    }
}

MEDIA_URL = 'http://10.40.8.206/media/'
ADMIN_MEDIA_PREFIX = 'http://10.40.8.206/admin/media/'