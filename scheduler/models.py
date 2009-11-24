from django.db import models
from datetime import datetime
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class PlayerProfile(models.Model):
    SPEED_CHOICES = ((u'SN', u'Snail'), (u'PD', u'Pedestrian'), (u'SP', u'Sprinter'), (u'RK', u'Rocket'),)
    STAMINA_CHOICES = ((u'SL', u'Sleep Walker'), (u'PR', u'Programmer'), (u'PD', u'Paladin LV7'), (u'MR', u'Marathonist'),)
    CONTROLL_CHOICES = ((u'LP', u'Light Post'), (u'EV', u'Evitationist'), (u'NW', u'Needle Worker'), (u'RN', u'Ronaldinho'),)
    SHOT_CHOICES = ((u'DP', u'Delicate'), (u'KK', u'Kicker'), (u'GD', u'Gigi Duru'), (u'GN', u'Gunner'),)
    user = models.ForeignKey(User, null=True, unique=True)
    alias_name = models.CharField(max_length=50)
    email_subscriptions = models.CharField(help_text='Subscription (FB-football,BB-basket,VB-volley):', max_length=50, default='FB')
    speed = models.CharField(null=True,blank=True, max_length=3, choices=SPEED_CHOICES)
    stamina = models.CharField(null=True,blank=True, max_length=3, choices=STAMINA_CHOICES)
    ball_controll = models.CharField(null=True,blank=True, max_length=3, choices=CONTROLL_CHOICES)
    shot_power = models.CharField(null=True,blank=True, max_length=3, choices=SHOT_CHOICES)

    @models.permalink
    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })

    def __unicode__(self):
        return self.user.username + "'s profile"

    def is_filled(self):
        return self.user.first_name != '' or self.user.last_name != '' or self.alias_name != ''

    def get_full_name(self):
        if self.is_filled():
            return self.user.first_name + ' ' + self.alias_name  + ' ' + self.user.last_name
        else:
            return self.user.username

    def __get_attendance_rate(self, sport):
        mds = MatchDay.objects.filter(sport= sport)
        count = mds.filter(participants__username= self.user.username).count()
        mdsCount = mds.count()
        procentage = "NA"
        if mdsCount > 0:
            procentage = str(count*100/mdsCount) + "%"
        return (str(count) + "/" + str(mdsCount), '<span class="procentage">'+ procentage + '</span>')

    def get_football_attendance_procentage(self):
        return self.__get_attendance_rate(MatchDay.FOOTBALL)[1]

    def get_basketball_attendance_procentage(self):
        return self.__get_attendance_rate(MatchDay.BASKETBALL)[1]

    def get_volleyball_attendance_procentage(self):
        return self.__get_attendance_rate(MatchDay.VOLLEYBALL)[1]

    def get_football_attendance_rate(self):
        return self.__get_attendance_rate(MatchDay.FOOTBALL)[0]
    
    def get_basketball_attendance_rate(self):
        return self.__get_attendance_rate(MatchDay.BASKETBALL)[0]

    def get_volleyball_attendance_rate(self):
        return self.__get_attendance_rate(MatchDay.VOLLEYBALL)[0]

class GuestPlayer(models.Model):
    friend_user = models.ForeignKey(User, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def __unicode__(self):
        return self.get_full_name() + ' invited by ' + self.friend_user.get_full_name()

    class Meta:
        unique_together = ('friend_user', 'first_name', 'last_name')

class MatchDay(models.Model):
    FOOTBALL = u'FB'
    VOLLEYBALL = u'VB'
    BASKETBALL = u'BB'
    SPORT_CHOICES = ((FOOTBALL, u'Football'), (VOLLEYBALL, u'Volleyball'), (BASKETBALL, u'Basketball'),)
    start_date = models.DateTimeField()
    location = models.CharField(max_length=50)
    sport = models.CharField(max_length=3, choices=SPORT_CHOICES, default=u'FB')
    participants = models.ManyToManyField(User, null=True, blank=True)
    guest_stars = models.ManyToManyField(GuestPlayer, null=True, blank=True)

    def __unicode__(self):
        return self.start_date.strftime('%d-%B-%Y')\
        + ' ' + self.location\
        + ' ' + self.start_date.strftime('%H:%M')

    def isFuture(self):
        return datetime.today() < self.start_date
    isFuture.short_description = 'Is in the future?'
    isFuture.boolean = True

    class Meta:
        ordering = ["-start_date"]

    @models.permalink
    def get_absolute_url(self):
        return ('sch_matchday_detail', (), {'object_id': self.id })


class Team(models.Model):
    name = models.CharField(max_length=50)
    matchday = models.ForeignKey(MatchDay)
    participants = models.ManyToManyField(User, null=True, blank=True)
    guest_stars = models.ManyToManyField(GuestPlayer, null=True, blank=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('sch_team_management', (), { 'object_id': self.matchday.id })

    class Meta:
        unique_together = ('name', 'matchday')

def user_profile_handler(sender, **kwargs):
    newUser = kwargs['instance']
    if kwargs['created']:
        try:
            newUser.get_profile()
        except:
            pp = PlayerProfile(user = newUser)
            pp.save()

class Proposal(models.Model):
    user = models.ForeignKey(User)
    matchday = models.ForeignKey(MatchDay)
    teams = models.TextField()

    def __unicode__(self):
        return self.user.get_full_name() + "'s proposal for " + str(self.matchday)

    class Meta:
        unique_together = ('user', 'matchday')

post_save.connect(user_profile_handler, sender=User)
