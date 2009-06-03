from django import forms
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationFormUniqueEmail
from registration.models import RegistrationProfile
from models import PlayerProfile, GuestPlayer

attrs_dict = { 'class': 'required' }

class PlayerRegistrationForm(RegistrationFormUniqueEmail):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    def save(self):
        new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],
                                                                    password=self.cleaned_data['password1'],
                                                                    email=self.cleaned_data['email'])
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.save() 
        return new_user

class GuestPlayerForm(forms.ModelForm):
    class Meta:
        model = GuestPlayer
        exclude = ('friend_user',)
