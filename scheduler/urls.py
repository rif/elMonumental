from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from scheduler.views import *
from django.contrib.auth.models import User
from models import MatchDay

md_info = {
    'queryset': MatchDay.objects.all(),
}


urlpatterns = patterns('django.contrib.auth.views',
    url(r'^$', object_list, md_info, name='matchday-list'),
    url(r'^attend/(?P<md_id>\d+)/$', attend, name='matchday-attend'),
    url(r'^abandon/(?P<md_id>\d+)/$', abandon, name='matchday-abandon'),
    url(r'^matchday/(?P<object_id>\d+)/$', object_detail, md_info, name='matchday-detail'),
    url(r'^accounts/profile/$', profileInfo, name='profile-link'),
    url(r'^accounts/login/$', 'login', {'template_name': 'scheduler/login.html'}, name='login-link'),
    url(r'^accounts/signup/$', signup, name='signup-link'),
    url(r'^accounts/logout/$', 'logout', {'template_name': 'scheduler/login.html', 'next_page':'/'}, name='logout-link'),
    url(r'^profileedit/$', profile, name='profile-edit-link'),
    url(r'^links/$', linkQuerry, name='request-callback'),
    url(r'^addguest/(?P<md_id>\d+)/$', addGuest, name='guest-add-link'),
    url(r'^delguest/(?P<md_id>\d+)/$', delGuest, name='guest-del-link'),
    url(r'^links/delguest/$', delGuestCallback, name='delGuest-callback'),
    url(r'^sendemail/(?P<md_id>\d+)/$', sendEmail, name='send-email-link'),
)
