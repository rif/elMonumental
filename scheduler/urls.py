from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'elMonumental.scheduler.views.index'),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'scheduler/login.html'}),
)
