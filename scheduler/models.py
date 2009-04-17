from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class PlayerProfile(models.Model):
    user = models.ForeignKey(User, null=True, unique=True)
    alias_name = models.CharField(max_length=50)
    goals_scored = models.IntegerField(null=True,blank=True)
    speed = models.IntegerField(null=True, blank=True)
    stamina = models.IntegerField(null=True, blank=True)
    ball_controll = models.IntegerField(null=True, blank=True)
    shot_power = models.IntegerField(null=True, blank=True)
    transfer_sum = models.IntegerField(null=True, blank=True)

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

