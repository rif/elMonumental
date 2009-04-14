from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'scheduler.views.index'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'scheduler/login.html', 'next':'/'}, name='login-link'),
)
