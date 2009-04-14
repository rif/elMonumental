from django.db import models
from datetime import datetime

class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    alias_name = models.CharField(max_length=50)
    team = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.first_name + ' ' + self.alias_name + ' ' + self.last_name

class MatchDay(models.Model):
    start_date = models.DateTimeField()
    location = models.CharField(max_length=50)
    attendee_players = models.ManyToManyField(Player)
    scoreA = models.IntegerField(blank=True)
    scoreB = models.IntegerField(blank=True)

    def __unicode__(self):
        return self.start_date.strftime('%d-%B-%Y')\
        + ' ' + self.location\
        + ' ' + self.start_date.strftime('%H:%M')

    def  isFuture(self):
        return datetime.today() < self.start_date
