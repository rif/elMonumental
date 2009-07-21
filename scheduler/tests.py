from datetime import datetime
from django.core import mail
from django.contrib.auth.models import User
from django.test import TestCase
from scheduler.models import GuestPlayer, PlayerProfile, MatchDay, Team

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
        self.user = User.objects.create_user('rif', 'rif@user.ad', 'test')
        self.user.save()
        self.logged_in = self.client.login(username='rif', password='test')
        future = datetime(2080, 07, 10)
        self.md = MatchDay(start_date = future)
        self.md.save()
        past = datetime(2009, 06, 12)
        self.old_md = MatchDay(start_date = past)
        self.old_md.save()
        self.gp = GuestPlayer(first_name = 'Radu', last_name = 'Fericean')
        self.gp.friend_user = self.user
        self.gp.save()
        self.md.guest_stars.add(self.gp)
        self.old_md.guest_stars.add(self.gp)

    def test_guest_full_name(self):
        gp = GuestPlayer(first_name = 'Radu', last_name = 'Fericean')
        self.failUnlessEqual(gp.get_full_name(), 'Radu Fericean')

    def test_del_guest_callback(self):
        self.assertTrue(self.gp in self.md.guest_stars.iterator())
        response = self.client.post('/links/delguest/', {'md_id': self.md.id, 'guest_id': self.gp.id})
        self.failUnlessEqual(response.status_code, 200)
        self.assertFalse(self.gp in self.md.guest_stars.iterator())

    def test_old_del_guest_callback(self):
        self.assertTrue(self.gp in self.md.guest_stars.iterator())
        response = self.client.post('/links/delguest/', {'md_id': self.old_md.id, 'guest_id': self.gp.id})
        self.failUnlessEqual(response.status_code, 302)
        self.assertTrue(self.gp in self.old_md.guest_stars.iterator())

    def test_del_guest_list(self):
        self.assertTrue(self.gp in self.md.guest_stars.iterator())
        response = self.client.post('/delguest/%s/' % self.md.id)
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.context['guest_list'], [self.gp])

class MatchDayTest(TestCase):
    def test_is_future_future(self):
        future = datetime(2080, 07, 10)
        md = MatchDay(start_date = future)
        self.assertTrue(md.isFuture())

    def test_is_future_past(self):
        past = datetime(2009, 06, 12)
        md = MatchDay(start_date = past)
        self.assertFalse(md.isFuture())

    def test_is_future_today(self):
        today = datetime.today()
        md = MatchDay(start_date = today)
        self.assertFalse(md.isFuture())

    def test_have_matchdays(self):
        today = datetime.today()
        MatchDay(start_date=today).save()
        self.failUnlessEqual(len(MatchDay.objects.all()), 1)

    def test_matchday_found(self):
        today = datetime.today()
        md = MatchDay(start_date=today)
        md.save()
        self.failUnlessEqual(MatchDay.objects.get(id='1'), md)

class AdminTest(TestCase):
    def setUp(self):
        admin = User.objects.create_user('admin', 'admin@admin.ad', 'test')
        admin.is_superuser=True
        admin.save()
        future = datetime(2080, 07, 10)
        self.md = MatchDay(start_date=future)
        self.md.save()

    def test_index(self):
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 200)

    def test_send_mail(self):
        logged_in = self.client.login(username='admin', password='test')
        self.assertTrue(logged_in)
        response = self.client.post('/sendemail/1/', {'subject': 'test', 'message': 'test'})
        self.failUnlessEqual(len(mail.outbox), 1)
        self.failUnlessEqual(mail.outbox[0].subject, 'test')

    def test_feed(self):
        response = self.client.get('/feeds/latest/')
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(len(response.content), 768)

    def test_deleteOrphanGuests(self):
        logged_in = self.client.login(username='admin', password='test')
        self.assertTrue(logged_in)
        gp = GuestPlayer(first_name = 'Radu', last_name = 'Fericean')
        gp.save()
        self.failUnlessEqual(len(GuestPlayer.objects.all()), 1)
        response = self.client.get('/deleteOrphanGps/')
        self.failUnlessEqual(response.content, '<p>Done, deleted 1 guest playes.</p><a href="/">Home</a>')
        self.failUnlessEqual(len(GuestPlayer.objects.all()), 0)

    def test_deleteOrphanGuestsNotDeeleted(self):
        logged_in = self.client.login(username='admin', password='test')
        self.assertTrue(logged_in)
        gp = GuestPlayer(first_name = 'Radu', last_name = 'Fericean')
        gp.save()
        self.md.guest_stars.add(gp)
        self.failUnlessEqual(len(GuestPlayer.objects.all()), 1)
        response = self.client.get('/deleteOrphanGps/')
        self.failUnlessEqual(len(GuestPlayer.objects.all()), 1)

class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('rif', 'rif@user.ad', 'test')
        self.user.save()
        self.logged_in = self.client.login(username='rif', password='test')
        future = datetime(2080, 07, 10)
        self.md = MatchDay(start_date = future)
        self.md.save()
        past = datetime(2009, 06, 12)
        self.old_md = MatchDay(start_date = past)
        self.old_md.save()

    def test_attend(self):
        self.assertTrue(self.logged_in)
        self.client.get('/attend/%s/' % self.md.id)
        self.assertTrue(self.user in self.md.participants.iterator())

    def test_old_attend(self):
        self.assertTrue(self.logged_in)
        self.client.get('/attend/%s/' % self.old_md.id)
        self.assertFalse(self.user in self.old_md.participants.iterator())

    def test_double_attend(self):
        self.assertTrue(self.logged_in)
        self.client.get('/attend/%s/' % self.md.id)
        self.failUnlessEqual(1, self.md.participants.count())

    def test_abandon(self):
        self.assertTrue(self.logged_in)
        self.client.get('/attend/%s/' % self.md.id)
        self.client.get('/abandon/%s/' % self.md.id)
        self.assertFalse(self.user in self.md.participants.iterator())

    def test_double_abandon(self):
        self.assertTrue(self.logged_in)
        self.client.get('/abandon/%s/' % self.md.id)
        self.client.get('/abandon/%s/' % self.md.id)
        self.assertFalse(self.user in self.md.participants.iterator())

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
        team = Team.objects.create(name="Bursucii", matchday=self.md)
        self.assertTrue(team in Team.objects.all())
        response = self.client.post('/delteam/%s/' % self.md.id)
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.context['team_list'][0], team)


__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> gp = GuestPlayer(first_name = 'Radu', last_name = 'Fericean')
>>> gp.get_full_name() == 'Radu Fericean'
True
"""}

