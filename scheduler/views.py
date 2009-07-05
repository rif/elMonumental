from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from scheduler.models import MatchDay
from scheduler.forms import GuestPlayerForm

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
    return HttpResponseRedirect(reverse('sch_matchday-list'))

@login_required
def abandon(request, md_id):
    md = get_object_or_404(MatchDay, pk=md_id)

    if not __isMatchdayInFuture(request, md):
        return HttpResponseRedirect(reverse('sch_matchday-list'))

    if request.user in md.participants.iterator():
        md.participants.remove(request.user)
        request.user.message_set.create(message='You have cowardly abandoned the matchday #%s held on %s at %s starting from %s.'
                                        % (md.id, md.start_date.strftime('%a, %d %b %Y'), md.location, md.start_date.strftime('%H:%M')))
    else:
        request.user.message_set.create(message='You are not in the matchday #s participant list.' % md.id)

    return HttpResponseRedirect(reverse('sch_matchday-list'))

def linkQuerry(request):
    if request.method == 'POST':
        md = get_object_or_404(MatchDay, pk=request.POST['md_id'])
        href = ''
        if md.isFuture():
            if request.user in md.participants.iterator():
                href += '<a href="%s">Abandon</a>' % reverse('sch_matchday-abandon', args=[md.id])
            else:
                href += '<a href="%s" href="#">Attend</a>' % reverse('sch_matchday-attend', args=[md.id])
            href += ' <a onclick="showAddGuest(%s)" href="#">G++</a>' % repr(reverse('sch_addguest', args=[md.id]))
            href += ' <a onclick="showDelGuest(%s)" href="#">G--</a>' % repr(reverse('sch_delguest', args=[md.id]))
        return HttpResponse(href)

def addGuest(request, md_id):
    if not request.user.is_authenticated():
        return HttpResponse('<div class="message">Please login!</div>')
    md = get_object_or_404(MatchDay, pk=md_id)
    if not __isMatchdayInFuture(request, md):
        return HttpResponseRedirect(reverse('sch_matchday-list'))

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
            return HttpResponseRedirect(reverse('sch_matchday-list'))
    else:
        form = GuestPlayerForm()
    return render_to_response('scheduler/add_guest.html',
                              {'form': form, 'md_id': md_id},
                              context_instance=RequestContext(request))

def delGuest(request, md_id):
    if not request.user.is_authenticated():
        return HttpResponse('<div class="message">Please login!</div>')
    md = get_object_or_404(MatchDay, pk=md_id)

    if not __isMatchdayInFuture(request, md):
        return HttpResponseRedirect(reverse('sch_matchday-list'))

    gsl = [gs for gs in md.guest_stars.iterator() if gs.friend_user == request.user]
    if len(gsl) == 0:
        return HttpResponse('You did not added any guest players to this metchday!')
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
    return HttpResponseRedirect(reverse('sch_matchday-list'))


@login_required
def sendEmail(request, md_id):
    if request.method == 'POST':
        md = get_object_or_404(MatchDay, pk=md_id)
        if not __isMatchdayInFuture(request, md):
            return HttpResponseRedirect(reverse('sch_matchday-list'))
        if request.user.is_superuser:
            from django.core.mail import send_mail
            subject = request.POST['subject']
            message = request.POST['message']
            fromEmail = request.user.email
            toList = []
            for user in User.objects.all():
                try:
                    if user.get_profile().receive_email:
                        toList.append(user.email)
                except:
                    request.user.message_set.create(message='The user %s has not defined a profile!' % user.username)
            send_mail(subject, message, fromEmail, toList)
            request.user.message_set.create(message = 'Email sent to users!')
        else:
            request.user.message_set.create(message='You do not have permission to send email to the group!')
        return HttpResponseRedirect(reverse('sch_matchday-list'))

def comment(request, md_id):
    md = get_object_or_404(MatchDay, pk=md_id)
    return render_to_response('scheduler/comment.html',
                             {'matchday': md}, context_instance=RequestContext(request))
                             
