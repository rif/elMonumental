from django.conf.urls.defaults import *
from scheduler import views
from models import MatchDay
from forms import PlayerRegistrationForm

md_info = {
    'queryset': MatchDay.objects.all(),
}

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^$', 'object_list', md_info, name='sch_matchday-list'),
    url(r'^matchday/(?P<object_id>\d+)/$', 'object_detail', md_info, name='sch_matchday-detail'),
)

# override forms from registration
urlpatterns += patterns('',
    url(r'^accounts/register/$', 'registration.views.register', {'form_class' : PlayerRegistrationForm}, name='registration_register'),
)

urlpatterns += patterns('',
    url(r'^attend/(?P<md_id>\d+)/$', views.attend, name='sch_matchday-attend'),
    url(r'^abandon/(?P<md_id>\d+)/$', views.abandon, name='sch_matchday-abandon'),
    url(r'^links/$', views.linkQuerry, name='sch_request-ajax'),
    url(r'^addguest/(?P<md_id>\d+)/$', views.addGuest, name='sch_addguest'),
    url(r'^delguest/(?P<md_id>\d+)/$', views.delGuest, name='sch_delguest'),
    url(r'^links/delguest/$', views.delGuestCallback, name='sch_delGuest-ajax'),
    url(r'^sendemail/(?P<md_id>\d+)/$', views.sendEmail, name='sch_sendemail'),
    url(r'^getemailform/(?P<md_id>\d+)/$', views.getEmailForm, name='sch_getEmailForm-ajax'),
)
