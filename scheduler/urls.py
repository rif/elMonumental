from django.conf.urls.defaults import *
from scheduler import views
from django.views.generic import list_detail
from django.views.generic.simple import direct_to_template
from scheduler.models import MatchDay, Proposal
from scheduler.forms import PlayerRegistrationForm, PlayerProfileForm
from scheduler.feeds import LatestMatchDays, LatestNews

feeds = {'latest': LatestMatchDays, 'news': LatestNews}
md_info = {'queryset': MatchDay.objects.all()}
proposal_info = {'queryset': Proposal.objects.all()}

urlpatterns = patterns('',
    url(r'^$',
        list_detail.object_list,
        dict(md_info, paginate_by = 10),
        name='sch_matchday_list'),
    url(r'^matchday/(?P<object_id>\d+)/$',
        list_detail.object_detail,
        md_info,
        name='sch_matchday_detail'),
    url(r'^matchday/(?P<object_id>\d+)/rss/$',
        list_detail.object_detail,
        dict(md_info, template_name = 'feeds/matchday_rssdetail.html'),
        name='sch_rss_detail'),
    url(r'^getemailform/(?P<object_id>\d+)/$',
        list_detail.object_detail,
        dict(md_info, template_name = 'scheduler/send_email_form.html'),
        name='sch_email_ajax'),
    url(r'^proposal/(?P<object_id>\d+)/$',
        list_detail.object_detail,
        dict(proposal_info, template_name = 'scheduler/proposal_detail.html'),
        name='sch_proposal_ajax'),
)

urlpatterns += patterns('',
    url(r'^accounts/register/$',
        'registration.views.register',
        {'form_class' : PlayerRegistrationForm,
         'backend': 'scheduler.forms.PlayerRegistrationBackend'},
        name='registration_register'),
    url(r'^profiles/edit/$',
        'profiles.views.edit_profile',
        {'form_class' : PlayerProfileForm},
        name='profiles_edit_profile'),
    url(r'^profiles/$',
        'profiles.views.profile_list',        
        name='profiles_profile_list'),
    url(r'^feeds/(?P<url>.*)/$',
        'django.contrib.syndication.views.feed',
        {'feed_dict': feeds}),
    url(r'^messages/$',
        direct_to_template,
        {'template': 'scheduler/messages.html'})
)

urlpatterns += patterns('',
    url(r'^attend/(?P<md_id>\d+)/$', views.attend, name='sch_matchday_attend'),
    url(r'^abandon/(?P<md_id>\d+)/$', views.abandon, name='sch_matchday_abandon'),
    url(r'^links/$', views.linkQuerry, name='sch_request-ajax'),
    url(r'^addguest/(?P<md_id>\d+)/$', views.addGuest, name='sch_guest_add'),
    url(r'^delguest/(?P<md_id>\d+)/$', views.delGuest, name='sch_guest_del'),
    url(r'^links/delguest/$', views.delGuestCallback, name='sch_guest_ajax_del'),
    url(r'^addteam/(?P<md_id>\d+)/$', views.addTeam, name='sch_team_add'),
    url(r'^delteam/(?P<md_id>\d+)/$', views.delTeam, name='sch_team_del'),
    url(r'^links/delteam/$', views.delTeamCallback, name='sch_team_ajax_del'),
    url(r'^sendemail/(?P<md_id>\d+)/$', views.sendEmail, name='sch_email_send'),
    url(r'^comments/(?P<md_id>\d+)/$', views.comment, name='sch_comments'),
    url(r'^loadTeam/$', views.loadTeam, name='sch_team_ajax'),
    url(r'^addProposal/$', views.addProposal, name='sch_addproposal'),
    url(r'^proposal/(?P<pid>\d+)/delete/$', views.delProposal, name='sch_proposal_del'),
    url(r'^matchday/(?P<object_id>\d+)/teams/$', views.teamsManagement, name='sch_team_management'),
    url(r'deleteOrphanGps/$', views.deleteOrphanGuestPlayers, name='sch_orphangp_del'),
    url(r'uniqueGps/$', views.makeGuestPlayersUnique, name='sch_gp_unique'),
    url(r'mdbysport/(?P<sport>\w+)/$', views.matchday_by_sport, name='sch_matchday_by_sport'),
)
