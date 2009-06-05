from django.conf.urls.defaults import *
from scheduler import views
from models import MatchDay
from forms import PlayerRegistrationForm
from feeds import LatestMatchDays

feeds = {'latest': LatestMatchDays,}
md_info = {'queryset': MatchDay.objects.all(),}
paginate_info = {'queryset': MatchDay.objects.all(), 'paginate_by': 10,}
rssdetail_info = {'queryset': MatchDay.objects.all(), 'template_name': 'feeds/matchday_rssdetail.html',}
email_info = {'queryset': MatchDay.objects.all(), 'template_name': 'scheduler/send_email_form.html',}

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^$', 'object_list', paginate_info, name='sch_matchday-list'),
    url(r'^matchday/(?P<object_id>\d+)/$', 'object_detail', md_info, name='sch_matchday-detail'),
    url(r'^matchday/rss/(?P<object_id>\d+)/$', 'object_detail', rssdetail_info, name='sch_matchday-detail'),
    url(r'^getemailform/(?P<object_id>\d+)/$', 'object_detail', email_info, name='sch_getEmailForm-ajax'),
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
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)
