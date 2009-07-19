from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from scheduler.models import MatchDay, GuestPlayer, Team, Proposal
from scheduler.forms import GuestPlayerForm, TeamForm

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
        request.user.message_set.create(message='You are not in the matchday %s participant list.' % md.id)

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
            found = False
            for guest in GuestPlayer.objects.filter(friend_user__pk = request.user.id):
                if guest.get_full_name() == gp.get_full_name():
                    md.guest_stars.add(guest)
                    found = True
                    break
            if not found:
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
                             {'guest_list': gsl, 'md_id': md_id},
                              context_instance=RequestContext(request))

@login_required
def delGuestCallback(request):
    if request.method == 'POST':
        md = get_object_or_404(MatchDay, pk=request.POST['md_id'])

        if not __isMatchdayInFuture(request, md):
            return HttpResponseRedirect(reverse('sch_matchday-list'))
        try:
            gp = md.guest_stars.get(id=request.POST['guest_id'])
        except:
            pass
        if gp != None:
            md.guest_stars.remove(gp)
            gp.delete()
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

def addTeam(request, md_id):
    if not request.user.is_authenticated():
        return HttpResponse('<div class="message">Please login!</div>')
    md = get_object_or_404(MatchDay, pk=md_id)
    if not __isMatchdayInFuture(request, md):
        return HttpResponseRedirect(reverse('sch_matchday-list'))

    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.matchday = md
            team.save()
            request.user.message_set.create(message='You added team %s to the matchday #%s.'
                                        % (team.name, md.id))
            return HttpResponseRedirect(reverse('sch_matchday-teams', args=[md.id]))
    else:
        form = TeamForm()
    return render_to_response('scheduler/add_team.html',
                              {'form': form, 'md_id': md_id},
                              context_instance=RequestContext(request))

def delTeam(request, md_id):
    if not request.user.is_authenticated():
        return HttpResponse('<div class="message">Please login!</div>')
    md = get_object_or_404(MatchDay, pk=md_id)

    if not __isMatchdayInFuture(request, md):
        return HttpResponseRedirect(reverse('sch_matchday-list'))

    teamList = Team.objects.filter(matchday__pk = md_id)
    if len(teamList) == 0:
        return HttpResponse('You did not added any teams to this metchday!')
    return render_to_response('scheduler/del_team.html',
                             {'team_list': teamList, 'md_id': md_id},
                              context_instance=RequestContext(request))

@login_required
def delTeamCallback(request):
    if request.method == 'POST':
        if not __isMatchdayInFuture(request, md):
            return HttpResponseRedirect(reverse('sch_matchday-list'))
        try:
            team = Team.objects.get(id=request.POST['team_id'])
        except:
            pass
        if team != None:
            team.delete()
            request.user.message_set.create(message='You removed team %s.' % team.name)
            return HttpResponse('')
    return HttpResponse('Cam aiurea!')


@login_required
def loadTeam(request):
    if request.method == 'POST':
        team = get_object_or_404(Team, pk=request.POST['teamId'])
        plIds = request.POST['pList'].strip()
        glIds = request.POST['gList'].strip()
        if request.user.is_superuser:
            team.participants.clear()
            team.guest_stars.clear()
            if plIds != '':
                for plId in plIds.split(','):
                    pl = User.objects.get(pk=plId)
                    team.participants.add(pl)
            if glIds != '':
                for gpId in glIds.split(','):
                    gp = GuestPlayer.objects.get(pk=gpId)
                    team.guest_stars.add(gp)
            team.save()
            request.user.message_set.create(message='Team saved!')
        else:
            text = ""
            if plIds != '':
                for plId in plIds.split(','):
                    pl = User.objects.get(pk=plId)
                    text += pl.get_full_name()
            if glIds != '':
                for gpId in glIds.split(','):
                    gp = GuestPlayer.objects.get(pk=gpId)
                    text += gp.get_full_name()
            if text != "":
                prop = Proposal.objects.create(user=request.user, matchday=team.matchday, teams=text)
                request.user.message_set.create(message='Proposal saved!')
        return HttpResponse('Done team ' + request.POST['teamId'])
    return HttpResponseRedirect(reverse('sch_matchday-list'))

@login_required
def deleteOrphanGuestPlayers(request):
    if request.user.is_superuser:
        guestPlayers = GuestPlayer.objects.all()
        matchdays = MatchDay.objects.all()
        foundGps = []
        deleted = 0
        for md in matchdays:
            for gp in md.guest_stars.iterator():
                if gp not in foundGps:
                    foundGps.append(gp)

        for gp in guestPlayers:
            if gp not in foundGps:
                gp.delete()
                deleted += 1
        return HttpResponse('<p>Done, deleted %s guest playes.</p><a href="/">Home</a>' % deleted)
    return HttpResponse('Please come back as the admin!')

def proposals(request, md_id):
    proposal_list = Proposal.objects.filter(matchday__pk=md_id)
    return render_to_response('scheduler/proposal_list.html',
                             {'proposal_list': proposal_list, 'md_id': md_id},
                              context_instance=RequestContext(request))

@login_required
def delProposal(request, pid):
    prop = get_object_or_404(Proposal, pk=pid)
    md = prop.matchday

    if not __isMatchdayInFuture(request, md):
        return HttpResponseRedirect(reverse('sch_matchday-list'))

    if prop.user != request.user:
        return HttpResponseRedirect(reverse('sch_matchday-list'))
    prop.delete()
    return HttpResponse('Proposal deleted!')