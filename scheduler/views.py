from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from models import MatchDay

@login_required
def attend(request, object_id):
    md = get_object_or_404(MatchDay, pk=object_id)
    return render_to_response('scheduler/attend.html', {'matchday':md})

