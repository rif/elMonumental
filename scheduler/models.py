from django.db import models

class MatchDay(models.Model):
	matchdate_date = models.DateTimeField()
	location = models.CharField(max_length=50)

	def __unicode__(self):
		return self.matchdate_date.strftime('%d-%B-%Y')\
		+ ' ' + self.location\
		+ ' ' + self.matchdate_date.strftime('%H:%M')



class Player(models.Model):
	attended_matches = models.ManyToManyField(MatchDay)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	alias_name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.first_name + ' ' + self.alias_name + ' ' + self.last_name