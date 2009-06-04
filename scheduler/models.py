from django.db import models
from datetime import datetime
from django.db.models.signals import post_save
from django.contrib.auth.models import User


SPEED_CHOICES = ((u'SN', u'Snail'), (u'PD', u'Pedestrian'), (u'SP', u'Sprinter'), (u'RK', u'Rocket'),)
STAMINA_CHOICES = ((u'SL', u'Sleep Walker'), (u'PR', u'Programmer'), (u'PD', u'Paladin LV7'), (u'MR', u'Marathonist'),)
CONTROLL_CHOICES = ((u'LP', u'Light Post'), (u'EV', u'Evitationist'), (u'NW', u'Needle Worker'), (u'RN', u'Ronaldinho'),)
SHOT_CHOICES = ((u'DP', u'Delicate'), (u'KK', u'Kicker'), (u'GD', u'Gigi Duru'), (u'GN', u'Gunner'),)


class PlayerProfile(models.Model):
    user = models.ForeignKey(User, null=True, unique=True)
    alias_name = models.CharField(max_length=50)
    receive_email = models.BooleanField('Do you want to by notified by email?', default=True)
    speed = models.CharField(null=True,blank=True, max_length=3, choices=SPEED_CHOICES)
    stamina = models.CharField(null=True,blank=True, max_length=3, choices=STAMINA_CHOICES)
    ball_controll = models.CharField(null=True,blank=True, max_length=3, choices=CONTROLL_CHOICES)
    shot_power = models.CharField(null=True,blank=True, max_length=3, choices=SHOT_CHOICES)

    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
    get_absolute_url = models.permalink(get_absolute_url)

    def __unicode__(self):
        return self.user.username + "'s profile"
    
    def isFilled(self):
        return self.alias_name == ''

class GuestPlayer(models.Model):
    friend_user = models.ForeignKey(User, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name


class MatchDay(models.Model):
    start_date = models.DateTimeField()
    location = models.CharField(max_length=50)
    participants = models.ManyToManyField(User, null=True, blank=True)
    guest_stars = models.ManyToManyField(GuestPlayer, null=True, blank=True)

    def __unicode__(self):
        return self.start_date.strftime('%d-%B-%Y')\
        + ' ' + self.location\
        + ' ' + self.start_date.strftime('%H:%M')

    def  isFuture(self):
        return datetime.today() < self.start_date

    class Meta:
        ordering = ["-start_date"]

def user_profile_handler(sender, **kwargs):
    newUser = kwargs['instance']
    if kwargs['created']:
        try:
            newUser.get_profile()
        except:
            pp = PlayerProfile(user = newUser)
            pp.save()

post_save.connect(user_profile_handler, sender=User)
