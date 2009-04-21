from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
from django.views.generic.list_detail import object_list, object_detail
from scheduler.views import attend, signup, profile
from models import MatchDay

info = {
    'queryset': MatchDay.objects.all(),
}

urlpatterns = patterns('',
    url(r'^$', object_list, info, name='matchday-list'),
    url(r'^attend/(?P<object_id>\d+)/$', attend, name='matchday-attend'),
    url(r'^matchday/(?P<object_id>\d+)/$', object_detail, info, name='matchday-detail'),
    url(r'^accounts/login/$', login, {'template_name': 'scheduler/login.html'}, name='login-link'),
    url(r'^accounts/signup/$', signup, name='signup-link'),
    url(r'^accounts/logout/$', logout, {'template_name': 'scheduler/login.html', 'next_page':'/'}, name='logout-link'),
    url(r'^accounts/profile/$', profile, name='profile-link'),
)
