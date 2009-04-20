from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from models import MatchDay, PlayerProfileForm, PlayerProfile

@login_required
def attend(request, object_id):
    md = get_object_or_404(MatchDay, pk=object_id)
    md.participants.add(request.user)
    return render_to_response('scheduler/attend.html',
                              {'matchday':md},
                              context_instance=RequestContext(request))

def signup(request):
    if request.method == 'POST': # If the form has been submitted...
        form = UserCreationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            newUser = form.save()
            user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password1'])
            login(request, user)
            return HttpResponseRedirect('/accounts/profile/%s' % user.id) # Redirect after POST
    else:
        form = UserCreationForm() # An unbound form
    return render_to_response('scheduler/signup.html',
                              {'form': form,},
                              context_instance=RequestContext(request))

def profile(request):
    if request.method == 'POST': # If the form has been submitted...
        form = PlayerProfileForm(request.POST) # A form bound to the POST data
        form.user = request.user
        if form.is_valid(): # All validation rules pass
            user = request.user
            profile = user.get_profile()
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            profile.alias_name = form.cleaned_data['alias_name']
            profile.goals_scored = form.cleaned_data['goals_scored']
            profile.speed = form.cleaned_data['speed']
            profile.stamina = form.cleaned_data['stamina']
            profile.ball_controll = form.cleaned_data['ball_controll']
            profile.shot_power = form.cleaned_data['shot_power']
            profile.transfer_sum = form.cleaned_data['transfer_sum']
            user.save()
            profile.save()
            return HttpResponseRedirect('/') # Redirect after POST
    else:
        try:
            pp = request.user.get_profile()
        except PlayerProfile.DoesNotExist:
            pp = PlayerProfile(user = request.user)
            pp.save()
        data = {'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'alias_name': pp.alias_name,
                'goals_scored': pp.goals_scored,
                'speed': pp.speed,
                'stamina': pp.stamina,
                'ball_controll': pp.ball_controll,
                'shot_power': pp.shot_power,
                'transfer_sum': pp.transfer_sum,
                }
        form = PlayerProfileForm(data) # An unbound form
    return render_to_response('scheduler/profile.html',
                              {'form': form,},
                              context_instance=RequestContext(request))