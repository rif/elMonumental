from django import forms
from registration.forms import RegistrationFormUniqueEmail
from registration.models import RegistrationProfile
from scheduler.models import GuestPlayer, Team, PlayerProfile, MatchDay
from registration.backends.default import DefaultBackend
import logging

attrs_dict = { 'class': 'required' }

class PlayerRegistrationBackend(DefaultBackend):
     def get_form_class(self, request):
         return PlayerRegistrationForm

     def register(self, request, **kwargs):
          new_user = super(PlayerRegistrationBackend, self).register(request, **kwargs)
          new_user.first_name = kwargs['first_name']
          new_user.last_name = kwargs['last_name']
          new_user.save()
          print('Hello: ', new_user.first_name)
          logging.debug('Hello: ', new_user.first_name)
          return new_user

class PlayerRegistrationForm(RegistrationFormUniqueEmail):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

class PlayerProfileForm(forms.ModelForm):
    alias_name = forms.CharField(max_length=50, help_text='Name of a sport star of monumental proportions (e.g. Mutu).')
    email_subscriptions = forms.CharField(
                widget=forms.CheckboxSelectMultiple(choices=MatchDay.SPORT_CHOICES))
    class Meta:
        model = PlayerProfile
        exclude = ('user',)

class GuestPlayerForm(forms.ModelForm):
    class Meta:
        model = GuestPlayer
        exclude = ('friend_user',)

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ('matchday', 'participants', 'guest_stars')
