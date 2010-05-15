from datetime import datetime
from django.core import mail
from django.contrib.auth.models import User
from django.test import TestCase
from scheduler.models import GuestPlayer, PlayerProfile, MatchDay, Team, Proposal, Sport

class ProfileTest(TestCase):
    def test_is_filled_empty(self):
        user=User()
        pp = PlayerProfile(user=user)
        self.assertFalse(pp.is_filled())

    def test_is_filled_partial(self):
        user=User()
        pp = PlayerProfile(user=user, alias_name = 'b')
        self.assertTrue(pp.is_filled())

    def test_is_filled_full(self):
        user=User(first_name = 'a', last_name = 'c')
        pp = PlayerProfile(user=user, alias_name = 'b')
        self.assertTrue(pp.is_filled())

    def test_get_full_name_existing(self):
        user=User(first_name = 'a',  last_name = 'c')
        pp = PlayerProfile(user=user, alias_name = 'b')
        self.failUnlessEqual(pp.get_full_name(), 'a b c')

    def test_get_full_name_username(self):
        user=User(username='rif')
        pp = PlayerProfile(user=user)
        self.failUnlessEqual(pp.get_full_name(), 'rif')

class GuestTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('rif', 'test@test.te', 'test')
        self.user.save()
        self.logged_in = self.client.login(username='rif', password='test')
        future = datetime(2080, 07, 10)
        self.sport = Sport.objects.create(name = "Football")
        self.md = MatchDay.objects.create(start_date = future, sport_name = self.sport)
        past = datetime(2009, 06, 12)
        self.old_md = MatchDay.objects.create(start_date = past, sport_name = self.sport)
        self.gp = GuestPlayer.objects.create(friend_user=self.user, first_name='Radu', last_name='Fericean')
        self.md.guest_stars.add(self.gp)
        self.old_md.guest_stars.add(self.gp)

    def test_guest_full_name(self):
        gp = GuestPlayer(first_name = 'Radu', last_name = 'Fericean')
        self.failUnlessEqual(gp.get_full_name(), 'Radu Fericean')

    def test_del_guest_callback(self):
        ogp = GuestPlayer.objects.create(friend_user=self.user, first_name='Bobo', last_name='Crem')
        self.md.guest_stars.add(ogp)
        self.assertTrue(ogp in self.md.guest_stars.all())
        self.assertTrue(ogp in GuestPlayer.objects.all())
        response = self.client.post('/links/delguest/', {'md_id': self.md.id, 'guest_id': ogp.id})
        self.failUnlessEqual(response.status_code, 200)
        self.assertFalse(ogp in self.md.guest_stars.all())
        self.assertFalse(ogp in GuestPlayer.objects.all())

    def test_old_del_guest_callback(self):
        self.assertTrue(self.gp in self.md.guest_stars.all())
        response = self.client.post('/links/delguest/', {'md_id': self.old_md.id, 'guest_id': self.gp.id})
        self.failUnlessEqual(response.status_code, 302)
        self.assertTrue(self.gp in self.old_md.guest_stars.all())
        self.assertTrue(self.gp in GuestPlayer.objects.all())

    def test_more_than_one_del_guest_callback(self):
        self.assertTrue(self.gp in self.md.guest_stars.all())
        other_md = MatchDay.objects.create(start_date = datetime(2080, 07, 10), sport_name = self.sport)
        other_md.guest_stars.add(self.gp)
        self.assertTrue(self.gp in other_md.guest_stars.all())
        response = self.client.post('/links/delguest/', {'md_id': self.md.id, 'guest_id': self.gp.id})
        self.failUnlessEqual(response.status_code, 200)
        self.assertTrue(self.gp in other_md.guest_stars.all())
        self.assertTrue(self.gp in GuestPlayer.objects.all())

    def test_del_guest_list(self):
        self.assertTrue(self.gp in self.md.guest_stars.all())
        response = self.client.post('/delguest/%s/' % self.md.id)
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.context['guest_list'], [self.gp])

class MatchDayTest(TestCase):
    def test_is_future_future(self):
        future = datetime(2080, 07, 10)
        md = MatchDay(start_date = future)
        self.assertTrue(md.is_future())

    def test_is_future_past(self):
        past = datetime(2009, 06, 12)
        md = MatchDay(start_date = past)
        self.assertFalse(md.is_future())

    def test_is_future_today(self):
        today = datetime.today()
        md = MatchDay(start_date = today)
        self.assertFalse(md.is_future())

    def test_have_matchdays(self):
        today = datetime.today()
        MatchDay.objects.create(start_date=today, sport_name=Sport.objects.create(name="Football"))
        self.failUnlessEqual(len(MatchDay.objects.all()), 1)

    def test_matchday_found(self):
        today = datetime.today()
        md = MatchDay.objects.create(start_date=today, sport_name=Sport.objects.create(name="Football"))
        self.failUnlessEqual(MatchDay.objects.get(id='1'), md)

class AdminTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@admin.ad', 'test')
        future = datetime(2080, 07, 10)
        self.sport = Sport.objects.create(name = "Football")
        self.md = MatchDay.objects.create(start_date=future, sport_name = self.sport)
        past = datetime(2009, 06, 12)
        self.old_md = MatchDay.objects.create(start_date = past, sport_name = self.sport)
        self.team = Team.objects.create(name='A', matchday=self.md)
        self.client.login(username='admin', password='test')

    def test_send_mail(self):
        user = User.objects.create_user('test', 'test@test.ad', 'test')
        pp = user.get_profile()
        pp.email_subscription.add(self.sport)
        pp.save()
        response = self.client.post('/sendemail/1/', {'subject': 'test', 'message': 'test'})
        self.failUnlessEqual(response.status_code, 302)
        self.failUnlessEqual(len(mail.outbox), 1)
        self.failUnlessEqual(mail.outbox[0].subject, 'test')

    def test_feed(self):
        response = self.client.get('/feeds/latest/')
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.content.count('<title>'), 3)
        self.failUnlessEqual(response.content.count('<description>'), 3)

    def test_deleteOrphanGuests(self):
        GuestPlayer.objects.create(first_name = 'Radu', last_name = 'Fericean')
        self.failUnlessEqual(len(GuestPlayer.objects.all()), 1)
        response = self.client.get('/deleteOrphanGps/')
        self.failUnlessEqual(response.content, '<p>Done, deleted 1 guest playes.</p><a href="/">Home</a>')
        self.failUnlessEqual(len(GuestPlayer.objects.all()), 0)

    def test_deleteOrphanGuestsNotDeleted(self):
        gp = GuestPlayer.objects.create(first_name = 'Radu', last_name = 'Fericean')
        self.md.guest_stars.add(gp)
        self.failUnlessEqual(len(GuestPlayer.objects.all()), 1)
        response = self.client.get('/deleteOrphanGps/')
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(len(GuestPlayer.objects.all()), 1)

    def test_makeGuestsUnique(self):
        gp = GuestPlayer.objects.create(first_name = 'Radu', last_name = 'Fericean')
        self.md.guest_stars.add(gp)
        ogp = GuestPlayer.objects.create(first_name = 'Radu', last_name = 'Fericean')
        self.old_md.guest_stars.add(ogp)
        self.failUnlessEqual(len(GuestPlayer.objects.all()), 2)
        response = self.client.get('/uniqueGps/')
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(len(GuestPlayer.objects.all()), 1)
        self.failUnlessEqual(self.md.guest_stars.all()[0], self.old_md.guest_stars.all()[0])

    def test_makeGuestsUniqueNotDeleted(self):
        gp = GuestPlayer.objects.create(first_name = 'Radu', last_name = 'Fericean')
        self.md.guest_stars.add(gp)
        ogp = GuestPlayer.objects.create(first_name = 'Radu1', last_name = 'Fericean')
        self.old_md.guest_stars.add(ogp)
        self.failUnlessEqual(len(GuestPlayer.objects.all()), 2)
        response = self.client.get('/uniqueGps/')
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(len(GuestPlayer.objects.all()), 2)
        self.failIfEqual(self.md.guest_stars.all()[0], self.old_md.guest_stars.all()[0])

    def test_loadAdminTeam(self):
        u1 = User.objects.create(username='rif')
        u2 = User.objects.create(username='pif')
        g1 = GuestPlayer.objects.create(friend_user=u1, first_name='Alex', last_name='DelPiero')
        g2 = GuestPlayer.objects.create(friend_user=u1, first_name='Bobo', last_name='Crem')
        response = self.client.post('/loadTeam/', {'teamId': '1', 'pList': '1,2,3', 'gList': '1,2'})
        self.failUnlessEqual(response.status_code, 302)
        user_list = (self.admin, u1, u2)
        team_user_list = self.team.participants.all()
        self.failUnlessEqual(user_list[0], team_user_list[0])
        self.failUnlessEqual(user_list[1], team_user_list[1])
        self.failUnlessEqual(user_list[2], team_user_list[2])
        guest_list = (g1, g2)
        team_guest_list = self.team.guest_stars.all()
        self.failUnlessEqual(guest_list[0], team_guest_list[0])
        self.failUnlessEqual(guest_list[1], team_guest_list[1])

    def test_loadTeam404(self):
        response = self.client.post('/loadTeam/', {'teamId': '2', 'pList': '1', 'gList': '1'})
        self.failUnlessEqual(response.status_code, 404)

    def test_loadTeamMessage(self):
        self.client.post('/loadTeam/', {'teamId': '1', 'pList': '1,2,3', 'gList': '1,2'})
        self.failUnlessEqual(self.admin.message_set.all()[0].message, "Saved team A.")

    def test_loadAdminTeamWrongIds(self):
        response = self.client.post('/loadTeam/', {'teamId': '1', 'pList': '1,2,3', 'gList': '1,2'})
        self.failUnlessEqual(response.status_code, 302)
        user_list = (self.admin,)
        team_user_list = self.team.participants.all()
        self.failUnlessEqual(user_list[0], team_user_list[0])
        self.failUnlessEqual(len(self.team.guest_stars.all()), 0)

class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('rif', 'test@test.te', 'test')
        self.user.first_name="Radu"
        self.user.last_name="Fericean"
        self.user.save()
        self.logged_in = self.client.login(username='rif', password='test')
        future = datetime(2080, 07, 10)
        sport = Sport.objects.create(name="Football")
        self.md = MatchDay.objects.create(start_date = future, sport_name = sport)
        self.past = datetime(2009, 06, 12)
        self.old_md = MatchDay.objects.create(start_date = self.past, sport_name = sport)
        self.team = Team.objects.create(name='A', matchday=self.md)

    def test_attend(self):
        self.assertTrue(self.logged_in)
        self.client.get('/attend/%s/' % self.md.id)
        self.assertTrue(self.user in self.md.participants.all())

    def test_football_atendance(self):
        self.md.participants.add(self.user)
        response = self.client.get('/profiles/')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTrue('<td>1/2</td><td><span class="procentage">50%</span></td>' in response.content)

    def test_basketball_atendance(self):
        basket = Sport.objects.create(name="Basketball")
        bmd1 = MatchDay.objects.create(start_date = self.past, sport_name = basket)
        bmd2 = MatchDay.objects.create(start_date = self.past, sport_name = basket)
        bmd1.participants.add(self.user)
        bmd2.participants.add(self.user)
        response = self.client.get('/profiles/')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTrue('<td>2/2</td><td><span class="procentage">100%</span></td>' in response.content)

    def test_volleyball_atendance(self):
        vmd = MatchDay.objects.create(start_date = self.past, sport_name = Sport.objects.create(name="Volleyball"))
        vmd.participants.add(self.user)        
        response = self.client.get('/profiles/')
        self.failUnlessEqual(response.status_code, 200)        
        self.assertTrue('Volleyball' in response.content)
        self.assertTrue('<td>1/1</td><td><span class="procentage">100%</span></td>' in response.content)

    def test_old_attend(self):
        self.assertTrue(self.logged_in)
        self.client.get('/attend/%s/' % self.old_md.id)
        self.assertFalse(self.user in self.old_md.participants.all())

    def test_double_attend(self):
        self.assertTrue(self.logged_in)
        self.client.get('/attend/%s/' % self.md.id)
        self.failUnlessEqual(1, self.md.participants.count())

    def test_abandon(self):
        self.assertTrue(self.logged_in)
        self.client.get('/attend/%s/' % self.md.id)
        self.client.get('/abandon/%s/' % self.md.id)
        self.assertFalse(self.user in self.md.participants.all())

    def test_double_abandon(self):
        self.assertTrue(self.logged_in)
        self.client.get('/abandon/%s/' % self.md.id)
        self.client.get('/abandon/%s/' % self.md.id)
        self.assertFalse(self.user in self.md.participants.all())

    def test_get_links_attend(self):
        response = self.client.post('/links/', {'md_id': self.md.id,})
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.content, '<a href="/attend/1/" href="#">Attend</a> <a onclick="showAddGuest(\'/addguest/1/\')" href="#">G++</a> <a onclick="showDelGuest(\'/delguest/1/\')" href="#">G--</a>')

    def test_get_links_abandon(self):
        self.assertTrue(self.logged_in)
        self.client.get('/attend/1/')
        response = self.client.post('/links/', {'md_id': self.md.id,})
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.content, '<a href="/abandon/1/">Abandon</a> <a onclick="showAddGuest(\'/addguest/1/\')" href="#">G++</a> <a onclick="showDelGuest(\'/delguest/1/\')" href="#">G--</a>')

    def test_get_past_links(self):
        response = self.client.post('/links/', {'md_id': self.old_md.id,})
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.content, '')

    def test_del_team_callback(self):
        team = Team.objects.create(name="Bursucii", matchday=self.md)
        self.assertTrue(team in Team.objects.all())
        response = self.client.post('/links/delteam/', {'md_id': self.md.id, 'team_id': team.id})
        self.failUnlessEqual(response.status_code, 200)
        self.assertFalse(team in Team.objects.all())

    def test_old_del_team_callback(self):
        team = Team.objects.create(name="Bursucii", matchday=self.old_md)
        self.assertTrue(team in Team.objects.all())
        response = self.client.post('/links/delteam/', {'md_id': self.old_md.id, 'team_id': team.id})
        self.failUnlessEqual(response.status_code, 302)
        self.assertTrue(team in Team.objects.all())

    def test_del_team_list(self):
        self.assertTrue(self.team in Team.objects.all())
        response = self.client.post('/delteam/%s/' % self.md.id)
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.context['team_list'][0], self.team)

    def test_proposal(self):
        entries = "Team A,rif,pif,|,Team B,test,best,|,"
        response = self.client.post('/addProposal/', {'md_id': '1', 'entries': entries})
        self.failUnlessEqual(response.status_code, 200)

        prop = Proposal.objects.filter(matchday__pk=self.md.id).get(user__pk=self.user.id)
        self.assertTrue(prop is not None)
        self.failUnlessEqual(prop.teams, 'Team A<ol><li>rif</li><li>pif</li></ol>Team B<ol><li>test</li><li>best</li></ol>')

    def test_proposal_message(self):
        entries = "Team A,rif,pif,|,Team B,test,best,|,"
        response = self.client.post('/addProposal/', {'md_id': '1', 'entries': entries})
        self.failUnlessEqual(self.user.message_set.all()[0].message, "Saved proposal Radu Fericean's proposal for Football 10-July-2080  00:00.")

    def test_proposalSingle(self):
        entries = "Team A,rif,pif,|,"
        response = self.client.post('/addProposal/', {'md_id': '1', 'entries': entries})
        self.failUnlessEqual(response.status_code, 200)

        prop = Proposal.objects.filter(matchday__pk=self.md.id).get(user__pk=self.user.id)
        self.assertTrue(prop is not None)
        self.failUnlessEqual(prop.teams, 'Team A<ol><li>rif</li><li>pif</li></ol>')

    def test_proposalWrongEntries(self):
        self.assertTrue(self.logged_in)
        entries = ""
        response = self.client.post('/addProposal/', {'md_id': '1', 'entries': entries})
        self.failUnlessEqual(response.status_code, 200)
        try:
            Proposal.objects.filter(matchday__pk=self.md.id).get(user__pk=self.user.id)
            self.assertTrue(False)
        except:pass

    def test_proposalDoubleSave(self):
        self.assertTrue(self.logged_in)
        entries = "Team A,rif,pif,|,Team B,test,best,|,"
        response = self.client.post('/addProposal/', {'md_id': '1', 'entries': entries})
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.post('/addProposal/', {'md_id': '1', 'entries': entries})
        self.failUnlessEqual(response.status_code, 200)
        prop = Proposal.objects.filter(matchday__pk=self.md.id).get(user__pk=self.user.id)
        self.assertTrue(prop is not None)
        self.failUnlessEqual(prop.teams, 'Team A<ol><li>rif</li><li>pif</li></ol>Team B<ol><li>test</li><li>best</li></ol>')

    def test_proposalSpecialCaseTwoTeams(self):
        self.assertTrue(self.logged_in)
        entries = "Team A,rif,pif,|,Team B,test,best,|,"
        response = self.client.post('/addProposal/', {'md_id': '1', 'entries': entries})
        self.failUnlessEqual(response.status_code, 200)
        single = "Team A,rif,pif,|,"
        response = self.client.post('/addProposal/', {'md_id': '1', 'entries': single})
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.post('/addProposal/', {'md_id': '1', 'entries': entries})
        self.failUnlessEqual(response.status_code, 200)
        prop = Proposal.objects.filter(matchday__pk=self.md.id).get(user__pk=self.user.id)
        self.assertTrue(prop is not None)
        self.failUnlessEqual(prop.teams, 'Team A<ol><li>rif</li><li>pif</li></ol>Team B<ol><li>test</li><li>best</li></ol>')

    def test_uniqueTeamNames(self):
        try:
            Team.objects.create(name='A', matchday=self.md)
            self.assertTrue(False)
        except: pass

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> gp = GuestPlayer(first_name = 'Radu', last_name = 'Fericean')
>>> gp.get_full_name() == 'Radu Fericean'
True
"""}

