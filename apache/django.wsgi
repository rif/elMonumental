import os
import site
import sys

site.addsitedir('/var/virtualenvs/elMonumental/lib/python2.6/site-packages')
sys.path.append('/var/django/elMonumental')

os.environ['DJANGO_SETTINGS_MODULE'] = 'elMonumental.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
