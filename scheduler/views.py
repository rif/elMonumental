from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from models import MatchDay, PlayerProfileForm, PlayerProfile

@login_required
def attend(request, object_id):
    md = get_object_or_404(MatchDay, pk=object_id)
    md.participants.add(request.user)
    request.user.message_set.create(message='You have joined the matchday #%s held on %s at %s starting from %s.'
                                    % (md.id, md.start_date.strftime('%a, %d %b %Y'), md.location, md.start_date.strftime('%H:%M')))
    return HttpResponseRedirect('/')

@login_required
def abandon(request, object_id):
    md = get_object_or_404(MatchDay, pk=object_id)
    md.participants.remove(request.user)
    request.user.message_set.create(message='You have cowardly abandoned the matchday #%s held on %s at %s starting from %s.'
                                    % (md.id, md.start_date.strftime('%a, %d %b %Y'), md.location, md.start_date.strftime('%H:%M')))
    return HttpResponseRedirect('/')

def signup(request):
    if request.method == 'POST': # If the form has been submitted...
        form = UserCreationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            newUser = form.save()
            user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password1'])
            login(request, user)
            return HttpResponseRedirect('/accounts/profile/') # Redirect after POST
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
            profile.speed = form.cleaned_data['speed']
            profile.stamina = form.cleaned_data['stamina']
            profile.ball_controll = form.cleaned_data['ball_controll']
            profile.shot_power = form.cleaned_data['shot_power']
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
                'speed': pp.speed,
                'stamina': pp.stamina,
                'ball_controll': pp.ball_controll,
                'shot_power': pp.shot_power,
                }
        form = PlayerProfileForm(data) # An unbound form
    return render_to_response('scheduler/profile.html',
                              {'form': form,},
                              context_instance=RequestContext(request))

def linkQuerry(request, md_id):
    md = get_object_or_404(MatchDay, pk=md_id)
    href = ''
    if md.isFuture():
        if request.user in md.participants.iterator():
            href += '<a href="abandon/%s">Abandon</a>' % md.id
        else:
            href += '<a href="attend/%s">Attend</a>' % md.id
    href += ' <a href="matchday/%s">View</a>' % md.id
    return HttpResponse(href)
