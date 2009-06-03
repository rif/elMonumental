import os
import sys
sys.path.append('/var/django')
sys.path.append('/var/django/elMonumental')

os.environ['DJANGO_SETTINGS_MODULE'] = 'elMonumental.settings_production.py'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
