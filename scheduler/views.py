from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from models import MatchDay, UserProfileForm

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
            user = authenticate(username=newUser.username, password=newUser.password)
            #user.message_set.create(message = "%s have registered succesfuly." % newUser.username)
            return HttpResponseRedirect('/accounts/profile/') # Redirect after POST
    else:
        form = UserCreationForm() # An unbound form
    return render_to_response('scheduler/signup.html',
                              {'form': form,},
                              context_instance=RequestContext(request))

def profile(request):
    if request.method == 'POST': # If the form has been submitted...
        form = UserProfileForm(request.POST) # A form bound to the POST data
        form.user = request.user
        if form.is_valid(): # All validation rules pass
            user = request.user
            user.get_profile().alias_name = form.alias_name
            user.save()
            return HttpResponseRedirect('/') # Redirect after POST
    else:
        form = UserProfileForm() # An unbound form
    return render_to_response('scheduler/profile.html',
                              {'form': form,},
                              context_instance=RequestContext(request))