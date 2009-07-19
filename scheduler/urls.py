from django.conf.urls.defaults import *
from scheduler import views
from models import MatchDay, Proposal
from forms import PlayerRegistrationForm
from feeds import LatestMatchDays

feeds = {'latest': LatestMatchDays,}
md_info = {'queryset': MatchDay.objects.all(),}
paginate_info = {'queryset': MatchDay.objects.all(), 'paginate_by': 10,}
rssdetail_info = {'queryset': MatchDay.objects.all(), 'template_name': 'feeds/matchday_rssdetail.html',}
email_info = {'queryset': MatchDay.objects.all(), 'template_name': 'scheduler/send_email_form.html',}
teams_info = {'queryset': MatchDay.objects.all(), 'template_name': 'scheduler/teams.html',}
proposal_info = {'queryset': Proposal.objects.all(), 'template_name': 'scheduler/proposal_detail.html',}

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^$', 'object_list', paginate_info, name='sch_matchday-list'),
    url(r'^matchday/(?P<object_id>\d+)/$', 'object_detail', md_info, name='sch_matchday-detail'),
    url(r'^matchday/(?P<object_id>\d+)/rss/$', 'object_detail', rssdetail_info, name='sch_matchday-detail'),
    url(r'^matchday/(?P<object_id>\d+)/teams/$', 'object_detail', teams_info, name='sch_matchday-teams'),
    url(r'^getemailform/(?P<object_id>\d+)/$', 'object_detail', email_info, name='sch_getEmailForm-ajax'),
    url(r'^proposal/(?P<object_id>\d+)/$', 'object_detail', proposal_info, name='sch_proposal-ajax'),
)

# override forms from registration
urlpatterns += patterns('',
    url(r'^accounts/register/$', 'registration.views.register', {'form_class' : PlayerRegistrationForm}, name='registration_register'),
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)

urlpatterns += patterns('',
    url(r'^attend/(?P<md_id>\d+)/$', views.attend, name='sch_matchday-attend'),
    url(r'^abandon/(?P<md_id>\d+)/$', views.abandon, name='sch_matchday-abandon'),
    url(r'^links/$', views.linkQuerry, name='sch_request-ajax'),
    url(r'^addguest/(?P<md_id>\d+)/$', views.addGuest, name='sch_addguest'),
    url(r'^delguest/(?P<md_id>\d+)/$', views.delGuest, name='sch_delguest'),
    url(r'^links/delguest/$', views.delGuestCallback, name='sch_delGuest-ajax'),
    url(r'^addteam/(?P<md_id>\d+)/$', views.addTeam, name='sch_addteam'),
    url(r'^delteam/(?P<md_id>\d+)/$', views.delTeam, name='sch_delteam'),
    url(r'^links/delteam/$', views.delTeamCallback, name='sch_delTeam-ajax'),
    url(r'^sendemail/(?P<md_id>\d+)/$', views.sendEmail, name='sch_sendemail'),
    url(r'^comments/(?P<md_id>\d+)/$', views.comment, name='sch_comments'),
    url(r'^loadTeam/$', views.loadTeam, name='sch_loadteam'),
    url(r'^matchday/(?P<md_id>\d+)/proposals/$', views.proposals, name='sch_matchday-proposals'),
    url(r'^proposal/(?P<pid>\d+)/delete/$', views.delProposal, name='sch_delproposal'),
    url(r'deleteOrphanGps/$', views.deleteOrphanGuestPlayers, name='sch_delorphangps'),
)
