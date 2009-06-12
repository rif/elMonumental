from datetime import datetime
from django.core import mail
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from scheduler.models import GuestPlayer, PlayerProfile, MatchDay

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
    def test_guest_full_name(self):
        gp = GuestPlayer(first_name = 'Radu', last_name = 'Fericean')
        self.failUnlessEqual(gp.get_full_name(), 'Radu Fericean')

class MatchDayTest(TestCase):
    def test_is_future_future(self):
        future = datetime(2080, 07, 10)
        md = MatchDay(start_date = future)
        self.assertTrue(md.isFuture())

    def test_is_future_past(self):
        past = datetime.today()
        md = MatchDay(start_date = past)
        self.assertFalse(md.isFuture())

    def test_is_future_today(self):
        today = datetime.today()
        md = MatchDay(start_date = today)
        self.assertFalse(md.isFuture())

class SimpleTest(TestCase):
    def test_index(self):
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 200)
    
    def test_send_mail(self):
        self.client.post('/sendmail/md_id=2')
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, 'Subject here')

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> gp = GuestPlayer(first_name = 'Radu', last_name = 'Fericean')
>>> gp.get_full_name() == 'Radu Fericean'
True
"""}

