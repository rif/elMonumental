from django.db import models

class Player(models.Model):    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    alias_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.first_name + ' ' + self.alias_name + ' ' + self.last_name

class MatchDay(models.Model):
    matchdate_date = models.DateTimeField()
    location = models.CharField(max_length=50)
    attendee_players = models.ManyToManyField(Player)

    def __unicode__(self):
        return self.matchdate_date.strftime('%d-%B-%Y')\
        + ' ' + self.location\
        + ' ' + self.matchdate_date.strftime('%H:%M')
