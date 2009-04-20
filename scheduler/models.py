from django.db import models
from datetime import datetime
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django import forms

SPEED_CHOICES = (('SN', 'Snail'), ('PD', 'Pedestrian'), ('SP', 'Sprinter'), ('RK', 'Rocket'),)
STAMINA_CHOICES = (('SL', 'Sleep Walker'), ('PR', 'Programmer'), ('PD', 'Paladin LV7'), ('MR', 'Marathonist'),)
CONTROLL_CHOICES = (('LP', 'Light Post'), ('EV', 'Evitationist'), ('NW', 'Needle Worker'), ('RN', 'Ronaldinho'),)
SHOT_CHOICES = (('SN', 'Snail'), ('KK', 'Kicker'), ('GD', 'Gigi Duru'), ('GN', 'Gunner'),)


class PlayerProfile(models.Model):
    user = models.ForeignKey(User, null=True, unique=True)
    alias_name = models.CharField(max_length=50)
    goals_scored = models.IntegerField(null=True,blank=True)
    speed = models.CharField(null=True,blank=True, max_length=3, choices=SPEED_CHOICES)
    stamina = models.CharField(null=True,blank=True, max_length=3, choices=STAMINA_CHOICES)
    ball_controll = models.CharField(null=True,blank=True, max_length=3, choices=CONTROLL_CHOICES)
    shot_power = models.CharField(null=True,blank=True, max_length=3, choices=SHOT_CHOICES)
    transfer_sum = models.IntegerField(null=True, blank=True)

class PlayerProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    class Meta:
        model = PlayerProfile
        exclude = ('user',)


class MatchDay(models.Model):
    start_date = models.DateTimeField()
    location = models.CharField(max_length=50)
    participants = models.ManyToManyField(User)

    def __unicode__(self):
        return self.start_date.strftime('%d-%B-%Y')\
        + ' ' + self.location\
        + ' ' + self.start_date.strftime('%H:%M')

    def  isFuture(self):
        return datetime.today() < self.start_date


    class Meta:
        ordering = ["-start_date"]

def user_profile_handler(sender, **kwargs):
    if kwargs['created'] == True:
        pp = PlayerProfile(user=kwargs['instance'])
        pp.save()

post_save.connect(user_profile_handler, sender=User)