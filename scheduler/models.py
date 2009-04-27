from django.db import models
from datetime import datetime
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django import forms

SPEED_CHOICES = (('SN', 'Snail'), ('PD', 'Pedestrian'), ('SP', 'Sprinter'), ('RK', 'Rocket'),)
STAMINA_CHOICES = (('SL', 'Sleep Walker'), ('PR', 'Programmer'), ('PD', 'Paladin LV7'), ('MR', 'Marathonist'),)
CONTROLL_CHOICES = (('LP', 'Light Post'), ('EV', 'Evitationist'), ('NW', 'Needle Worker'), ('RN', 'Ronaldinho'),)
SHOT_CHOICES = (('DP', 'Delicate'), ('KK', 'Kicker'), ('GD', 'Gigi Duru'), ('GN', 'Gunner'),)


class PlayerProfile(models.Model):
    user = models.ForeignKey(User, null=True, unique=True)
    alias_name = models.CharField(max_length=50)
    speed = models.CharField(null=True,blank=True, max_length=3, choices=SPEED_CHOICES)
    stamina = models.CharField(null=True,blank=True, max_length=3, choices=STAMINA_CHOICES)
    ball_controll = models.CharField(null=True,blank=True, max_length=3, choices=CONTROLL_CHOICES)
    shot_power = models.CharField(null=True,blank=True, max_length=3, choices=SHOT_CHOICES)

class PlayerProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    class Meta:
        model = PlayerProfile
        exclude = ('user',)
        fields = ['first_name', 'last_name', 'email', 'alias_name', 'speed', 'stamina', 'ball_controll', 'shot_power']

class GuestPlayer(models.Model):
    friend_user = models.ForeignKey(User, null=True, unique=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

class GuestPlayerForm(forms.ModelForm):
    class Meta:
        model = GuestPlayer
        exclude = ('friend_user',)


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
    if kwargs['created'] and newUser.get_profile is None:
        pp = PlayerProfile(user = newUser)
        pp.save()

post_save.connect(user_profile_handler, sender=User)
