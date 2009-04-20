from django.conf.urls.defaults import *

from models import MatchDay

info = {
    'queryset': MatchDay.objects.all(),
}

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.list_detail.object_list', info, name='matchday-list'),
    url(r'^attend/(?P<object_id>\d+)/$', 'scheduler.views.attend', name='matchday-attend'),
    url(r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', info, name='matchday-detail'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'scheduler/login.html'}, name='login-link'),
    url(r'^accounts/signup/$', 'scheduler.views.signup', name='signup-link'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'scheduler/login.html', 'next_page':'/'}, name='logout-link'),
    url(r'^accounts/profile/$', 'scheduler.views.profile', name='profile-link'),
)
