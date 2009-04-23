from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from scheduler.views import *
from models import MatchDay

info = {
    'queryset': MatchDay.objects.all(),
}

urlpatterns = patterns('django.contrib.auth.views',
    url(r'^$', object_list, info, name='matchday-list'),
    url(r'^attend/(?P<object_id>\d+)/$', attend, name='matchday-attend'),
    url(r'^abandon/(?P<object_id>\d+)/$', abandon, name='matchday-abandon'),
    url(r'^matchday/(?P<object_id>\d+)/$', object_detail, info, name='matchday-detail'),
    url(r'^accounts/login/$', 'login', {'template_name': 'scheduler/login.html'}, name='login-link'),
    url(r'^accounts/signup/$', signup, name='signup-link'),
    url(r'^accounts/logout/$', 'logout', {'template_name': 'scheduler/login.html', 'next_page':'/'}, name='logout-link'),
    url(r'^accounts/profile/$', profile, name='profile-link'),
    url(r'^links/(?P<md_id>\d{1})/$', linkQuerry, name='request-callback'),
)
