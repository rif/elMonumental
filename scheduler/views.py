from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from models import MatchDay, PlayerProfileForm, PlayerProfile, GuestPlayerForm
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User


def __isMatchdayInFuture(request, md):
    if not md.isFuture():
        request.user.message_set.create(message='Selected matchday was played on %s.'
                                        % md.start_date.strftime('%a, %d %b %Y'))
    return md.isFuture()

@login_required
def attend(request, md_id):
    md = get_object_or_404(MatchDay, pk=md_id)
    if __isMatchdayInFuture(request, md):
        md.participants.add(request.user)
        request.user.message_set.create(message='You have joined the matchday #%s held on %s at %s starting from %s.'
                                        % (md.id, md.start_date.strftime('%a, %d %b %Y'), md.location, md.start_date.strftime('%H:%M')))
    return HttpResponseRedirect('/')

@login_required
def abandon(request, md_id):
    md = get_object_or_404(MatchDay, pk=md_id)

    if not __isMatchdayInFuture(request, md):
        return HttpResponseRedirect('/')

    if request.user in md.participants.iterator():
        md.participants.remove(request.user)
        request.user.message_set.create(message='You have cowardly abandoned the matchday #%s held on %s at %s starting from %s.'
                                        % (md.id, md.start_date.strftime('%a, %d %b %Y'), md.location, md.start_date.strftime('%H:%M')))
    else:
        request.user.message_set.create(message='You are not in the matchday #s participant list.' % md.id)

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
    UserInlineFormSet = inlineformset_factory(User, PlayerProfile)
    if request.method == 'POST': # If the form has been submitted...
        user = request.user
        profile = user.get_profile()

        form = PlayerProfileForm(request.POST, instance=profile) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            form.save()
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
                'receive_email': pp.receive_email,
                'speed': pp.speed,
                'stamina': pp.stamina,
                'ball_controll': pp.ball_controll,
                'shot_power': pp.shot_power,
                }
        form = PlayerProfileForm(data)
    return render_to_response('scheduler/profile.html',
                              {'form': form,},
                              context_instance=RequestContext(request))

def linkQuerry(request):
    if request.method == 'POST':
        md = get_object_or_404(MatchDay, pk=request.POST['md_id'])
        href = ''
        if md.isFuture():
            if request.user in md.participants.iterator():
                href += '<a href="abandon/%s">Abandon</a>' % md.id
            else:
                href += '<a href="attend/%s">Attend</a>' % md.id
            href += ' <a href="addguest/%s">G++</a>' % md.id
            href += ' <a href="delguest/%s">G--</a>' % md.id
        href += ' <a href="matchday/%s">View</a>' % md.id
        return HttpResponse(href)

@login_required
def addGuest(request, md_id):
    md = get_object_or_404(MatchDay, pk=md_id)
    if not __isMatchdayInFuture(request, md):
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = GuestPlayerForm(request.POST)
        if form.is_valid():
            gp = form.save(commit=False)
            gp.friend_user = request.user
            gp.save()
            md.guest_stars.add(gp)
            md.save()
            request.user.message_set.create(message='You added guest star %s to the matchday #%s.'
                                        % (gp.get_full_name() ,md.id))
            return HttpResponseRedirect('/')
    else:
        form = GuestPlayerForm()
    return render_to_response('scheduler/add_guest.html',
                              {'form': form, 'md_id': md_id},
                              context_instance=RequestContext(request))

@login_required
def delGuest(request, md_id):
    md = get_object_or_404(MatchDay, pk=md_id)

    if not __isMatchdayInFuture(request, md):
        return HttpResponseRedirect('/')

    gsl = [gs for gs in md.guest_stars.iterator() if gs.friend_user == request.user]
    if len(gsl) == 0:
        request.user.message_set.create(message='You did not added any guest players to this metchday!')
        return HttpResponseRedirect('/')
    return render_to_response('scheduler/del_guest.html',
                             {'guests_lists': gsl, 'md_id': md_id},
                              context_instance=RequestContext(request))

@login_required
def delGuestCallback(request):
    if request.method == 'POST':
        md = get_object_or_404(MatchDay, pk=request.POST['md_id'])
        gp = md.guest_stars.get(id=request.POST['guest_id'])
        if gp != None:
            md.guest_stars.remove(gp)
            request.user.message_set.create(message='You removed guest star %s from the matchday #%s.'
                                            % (gp.get_full_name(), md.id))
            return HttpResponse('')
    return HttpResponseRedirect('/')

@login_required
def sendEmail(request, md_id):
    md = get_object_or_404(MatchDay, pk=md_id)

    if not __isMatchdayInFuture(request, md):
        return HttpResponseRedirect('/')

    if request.user.is_superuser:
        from django.core.mail import send_mail
        subject = 'Fotball invite'
        message = 'Connect to http://elMonumental.sro.oce.net for matchday #%s.' % md_id
        fromEmail = request.user.email
        mass = ""
        for user in User.objects.all():
            try:
                if user.get_profile().receive_email:
                    mass += "(%s %s %s %s)" % (subject, message, fromEmail, user.email)
                    send_mail(subject, message, fromEmail, user.email)
                    request.user.message_set.create(message = 'Email sent to users!')
            except:
                request.user.message_set.create(message='The user %s has not defined a profile!' % user.username)
    else:
        request.user.message_set.create(message='You do not have permission to send email to the group!')
    return HttpResponseRedirect('/')