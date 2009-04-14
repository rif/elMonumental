from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def attend(request, object_id):
    return render_to_response('scheduler/attend.html', {})

