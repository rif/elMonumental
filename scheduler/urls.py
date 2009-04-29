from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from scheduler.views import *
from django.contrib.auth.models import User
from models import MatchDay

md_info = {
    'queryset': MatchDay.objects.all(),
}

user_info = {
    'queryset': User.objects.all(),
    'template_name': 'scheduler/user_detail.html',
}

urlpatterns = patterns('django.contrib.auth.views',
    url(r'^$', object_list, md_info, name='matchday-list'),
    url(r'^attend/(?P<md_id>\d+)/$', attend, name='matchday-attend'),
    url(r'^abandon/(?P<md_id>\d+)/$', abandon, name='matchday-abandon'),
    url(r'^matchday/(?P<object_id>\d+)/$', object_detail, md_info, name='matchday-detail'),
    url(r'^profile/(?P<object_id>\d+)/$', object_detail, user_info, name='profile-link'),
    url(r'^accounts/login/$', 'login', {'template_name': 'scheduler/login.html'}, name='login-link'),
    url(r'^accounts/signup/$', signup, name='signup-link'),
    url(r'^accounts/logout/$', 'logout', {'template_name': 'scheduler/login.html', 'next_page':'/'}, name='logout-link'),
    url(r'^accounts/profile/$', profile, name='profile-edit-link'),
    url(r'^links/(?P<md_id>\d{1})/$', linkQuerry, name='request-callback'),
    url(r'^addguest/(?P<md_id>\d+)/$', addGuest, name='guest-add-link'),
    url(r'^delguest/(?P<md_id>\d+)/$', delGuest, name='guest-del-link'),
)
