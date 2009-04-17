from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import UserManager
from models import MatchDay

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
            user = UserManager.create_user(form.username, 'test@oce.com' ,form.password1)
            user.message_set.create(message="Your user was created succesfuly.")
            return HttpResponseRedirect('/') # Redirect after POST
    else:
        form = UserCreationForm() # An unbound form
    return render_to_response('scheduler/signup.html',
                              {'form': form,},
                              context_instance=RequestContext(request))