from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.views.generic import list_detail
from scheduler.models import MatchDay, GuestPlayer, Team, Proposal, PlayerProfile, Sport
from scheduler.forms import GuestPlayerForm, TeamForm
from datetime import datetime
from profiles.views import profile_list

def __isMatchdayInFuture(request, md):
    if not md.isFuture():
        request.user.message_set.create(message='Selected matchday was played on %s.'
                                        % md.start_date.strftime('%a, %d %b %Y'))
    return md.isFuture()

def matchday_by_sport(request, sport):
    return list_detail.object_list(
        request,
        queryset = MatchDay.objects.filter(sport_name__name=sport),
        paginate_by = 10,
        template_name = "scheduler/filtered_matchday_list.html",
        extra_context = {"sport" : sport}
    )


@login_required
def attend(request, md_id):
    md = get_object_or_404(MatchDay, pk=md_id)
    if __isMatchdayInFuture(request, md):
        md.participants.add(request.user)
        request.user.message_set.create(message='You have joined the matchday #%s held on %s at %s starting from %s.'
                                        % (md.id, md.start_date.strftime('%a, %d %b %Y'), md.location, md.start_date.strftime('%H:%M')))
    return redirect('sch_matchday_list')

@login_required
def abandon(request, md_id):
    md = get_object_or_404(MatchDay, pk=md_id)

    if not __isMatchdayInFuture(request, md):
        return redirect('sch_matchday_list')

    if request.user in md.participants.all():
        md.participants.remove(request.user)
        request.user.message_set.create(message='You have cowardly abandoned the matchday #%s held on %s at %s starting from %s.'
                                        % (md.id, md.start_date.strftime('%a, %d %b %Y'), md.location, md.start_date.strftime('%H:%M')))
    else:
        request.user.message_set.create(message='You are not in the matchday %s participant list.' % md.id)

    return redirect('sch_matchday_list')

def linkQuerry(request):
    if request.method == 'POST':
        md = get_object_or_404(MatchDay, pk=request.POST['md_id'])
        href = ''
        if md.isFuture():
            if request.user in md.participants.all():
                href += '<a href="%s">Abandon</a>' % reverse('sch_matchday_abandon', args=[md.id])
            else:
                href += '<a href="%s" href="#">Attend</a>' % reverse('sch_matchday_attend', args=[md.id])
            href += ' <a onclick="showAddGuest(%s)" href="#">G++</a>' % repr(reverse('sch_guest_add', args=[md.id]))
            href += ' <a onclick="showDelGuest(%s)" href="#">G--</a>' % repr(reverse('sch_guest_del', args=[md.id]))
        return HttpResponse(href)

def addGuest(request, md_id):
    if not request.user.is_authenticated():
        return HttpResponse('<div class="message">Please login!</div>')
    md = get_object_or_404(MatchDay, pk=md_id)
    if not __isMatchdayInFuture(request, md):
        return redirect('sch_matchday_list')

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
            return redirect('sch_matchday_list')
    else:
        form = GuestPlayerForm()
    return render_to_response('scheduler/add_guest.html',
                              {'form': form, 'md_id': md_id})

def delGuest(request, md_id):
    if not request.user.is_authenticated():
        return HttpResponse('<div class="message">Please login!</div>')
    md = get_object_or_404(MatchDay, pk=md_id)

    if not __isMatchdayInFuture(request, md):
        return redirect('sch_matchday_list')

    gsl = [gs for gs in md.guest_stars.all() if gs.friend_user == request.user]
    if len(gsl) == 0:
        return HttpResponse('You did not added any guest players to this metchday!')
    return render_to_response('scheduler/del_guest.html',
                             {'guest_list': gsl, 'md_id': md_id})

@login_required
def delGuestCallback(request):
    if request.method == 'POST':
        md = get_object_or_404(MatchDay, pk=request.POST['md_id'])

        if not __isMatchdayInFuture(request, md):
            return redirect('sch_matchday_list')
        try:
            gp = md.guest_stars.get(id=request.POST['guest_id'])
        except:
            pass
        if gp != None:
            md.guest_stars.remove(gp)
            usedByOthers = False
            for md in MatchDay.objects.iterator():
                if gp in md.guest_stars.all():
                    usedByOthers = True
                    break
            if not usedByOthers:
                gp.delete()
            request.user.message_set.create(message='You removed guest star %s from the matchday #%s.'
                                            % (gp.get_full_name(), md.id))
            return HttpResponse('')
    return redirect('sch_matchday_list')


@login_required
def sendEmail(request, md_id):
    if request.method == 'POST':
        md = get_object_or_404(MatchDay, pk=md_id)
        if not __isMatchdayInFuture(request, md):
            return redirect('sch_matchday_list')
        if request.user.is_staff:
            from django.core.mail import send_mail
            subject = request.POST['subject']
            message = request.POST['message']
            fromEmail = request.user.email
            toList = []
            for user in User.objects.iterator():
                try:
                    if md.sport_name in user.get_profile().email_subscription.all():
                        toList.append(user.email)
                except:
                    request.user.message_set.create(message='The user %s has not defined a profile!' % user.username)
            send_mail(subject, message, fromEmail, toList)
            request.user.message_set.create(message = 'Email sent to users!')
        else:
            request.user.message_set.create(message='You do not have permission to send email to the group!')
        return redirect('sch_matchday_list')

def comment(request, md_id):
    md = get_object_or_404(MatchDay, pk=md_id)
    return render_to_response('scheduler/comment.html',
                             {'matchday': md},
                              context_instance=RequestContext(request))

def addTeam(request, md_id):
    if not request.user.is_authenticated() and not request.user.is_staff:
        return HttpResponse('<div class="message">Please login as super user!</div>')
    md = get_object_or_404(MatchDay, pk=md_id)
    if not __isMatchdayInFuture(request, md):
        return redirect('sch_matchday_list')

    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.matchday = md
            team.save()
            request.user.message_set.create(message='You added team %s to the matchday #%s.'
                                        % (team.name, md.id))
            return redirect('sch_team_management', md.id)
    else:
        form = TeamForm()
    return render_to_response('scheduler/add_team.html',
                              {'form': form, 'md_id': md_id})

def delTeam(request, md_id):
    if not request.user.is_authenticated() and not request.user.is_staff:
        return HttpResponse('<div class="message">Please login as super user!</div>')
    md = get_object_or_404(MatchDay, pk=md_id)

    if not __isMatchdayInFuture(request, md):
        return redirect('sch_matchday_list')

    teamList = Team.objects.filter(matchday__pk = md_id)
    if len(teamList) == 0:
        return HttpResponse('You did not added any teams to this metchday!')
    return render_to_response('scheduler/del_team.html',
                             {'team_list': teamList, 'md_id': md_id})

@login_required
def delTeamCallback(request):
    if request.method == 'POST':
        try:
            team = Team.objects.get(id=request.POST['team_id'])
            if not __isMatchdayInFuture(request, team.matchday):
                return redirect('sch_matchday_list')
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
        if request.user.is_staff:
            team.participants.clear()
            team.guest_stars.clear()
            if plIds != '':
                for plId in plIds.split(','):
                    try:
                        pl = User.objects.get(pk=plId)
                        team.participants.add(pl)
                    except: pass
            if glIds != '':
                for gpId in glIds.split(','):
                    try:
                        gp = GuestPlayer.objects.get(pk=gpId)
                        team.guest_stars.add(gp)
                    except: pass
            team.save()
            request.user.message_set.create(message='Saved team %s.' % team.name)
    return redirect('sch_matchday_list')

@login_required
def addProposal(request):
    md = get_object_or_404(MatchDay, pk = request.POST['md_id'])
    if not __isMatchdayInFuture(request, md):
        return redirect('sch_matchday_list')
    if request.method == 'POST':
        entries = request.POST['entries']
        entries = entries.split('|')
        text = ""
        for team in entries:
            team = team.strip(',')
            team = team.split(',')
            if team[0] != '':
                text += team[0] + "<ol>"
                for line in team[1:]:
                    if line != '':
                        text += "<li>" + line + "</li>"
                text += "</ol>"
        if text != "":
            try:
                prop = Proposal.objects.get(matchday__pk=md.id, user__pk=request.user.id)
                prop.teams = text
                prop.save()
            except:
                prop = Proposal.objects.create(user=request.user, matchday=md, teams=text)
            request.user.message_set.create(message='Saved proposal %s.' % str(prop))
    return HttpResponse('Done!')

@login_required
def deleteOrphanGuestPlayers(request):
    if request.user.is_superuser:
        foundGps = []
        deleted = 0
        for md in MatchDay.objects.iterator():
            for gp in md.guest_stars.iterator():
                if gp not in foundGps:
                    foundGps.append(gp)

        for gp in GuestPlayer.objects.iterator():
            if gp not in foundGps:
                gp.delete()
                deleted += 1
        return HttpResponse('<p>Done, deleted %s guest playes.</p><a href="/">Home</a>' % deleted)
    return HttpResponse('Please come back as the admin!')


@login_required
def makeGuestPlayersUnique(request):
    def __getOtherFoundGuest(gp_item):
        for gp in GuestPlayer.objects.iterator():
            if gp.id != gp_item.id and\
                    gp.friend_user == gp_item.friend_user and\
                    gp.get_full_name() == gp_item.get_full_name():
                return gp
        return None

    if request.user.is_superuser:
        deleted = 0
        for md in MatchDay.objects.iterator():
            for gp in md.guest_stars.iterator():
                other_gp = __getOtherFoundGuest(gp)
                if other_gp != None:
                    md.guest_stars.remove(gp)
                    md.guest_stars.add(other_gp)
                    md.save()
                    gp.delete()
                    deleted += 1
        return HttpResponse('<p>Done, deleted %s guest playes.</p><a href="/">Home</a>' % deleted)
    return HttpResponse('Please come back as the admin!')

def teamsManagement(request, object_id):
    proposal_list = Proposal.objects.filter(matchday__pk=object_id)

    return list_detail.object_detail(
        request,
        queryset = MatchDay.objects.all(),
        object_id = object_id,
        template_name = 'scheduler/teams.html',
        extra_context = {"proposal_list" : proposal_list}
    )


@login_required
def delProposal(request, pid):
    prop = get_object_or_404(Proposal, pk=pid)
    md = prop.matchday

    if not __isMatchdayInFuture(request, md):
        return redirect('sch_matchday_list')

    if prop.user != request.user:
        return redirect('sch_matchday_list')
    prop.delete()
    return HttpResponse('Proposal deleted!')

def profileList(request):
    extra_context = {'sport_list': Sport.objects.all()}
    if request.method == 'POST':
        since = request.POST['since']
        if since != '':
            since = datetime.strptime(since, "%d-%m-%Y")
            extra_context['since'] = since
        response = list_detail.object_list(
            request,
            extra_context = extra_context,
            queryset=PlayerProfile.objects.all(),
            template_name="profiles/profile_list.html",
            )
    else:
        response = profile_list(
            request,
            extra_context = extra_context,
            queryset=PlayerProfile.objects.all(),
            )
    return response

