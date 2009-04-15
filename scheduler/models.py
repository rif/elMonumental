from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    alias_name = models.CharField(max_length=50)
    goals_scored = models.IntegerField(blank=True)
    speed = models.IntegerField(blank=True)
    stamina = models.IntegerField(blank=True)
    ball_controll = models.IntegerField(blank=True)
    shot_power = models.IntegerField(blank=True)
    transfer_sum = models.IntegerField(blank=True)

class MatchDay(models.Model):
    start_date = models.DateTimeField()
    location = models.CharField(max_length=50)
    attendee_players = models.ManyToManyField(User, through='Team')
    scoreA = models.IntegerField(blank=True)
    scoreB = models.IntegerField(blank=True)

    def __unicode__(self):
        return self.start_date.strftime('%d-%B-%Y')\
        + ' ' + self.location\
        + ' ' + self.start_date.strftime('%H:%M')

    def  isFuture(self):
        return datetime.today() < self.start_date

class Team(models.Model):
    name = models.CharField(max_length=50)
    matchDay = models.ForeignKey(MatchDay)
    members = models.ForeignKey(User)
