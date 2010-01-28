from django import template
from scheduler.models import MatchDay

def do_atendance_procentage(parser, token):
        bits = token.contents.split()
        username = bits[0]
        sport = bits[1]
        return "tata"
        mds = MatchDay.objects.filter(sport= sport)
        count = mds.filter(participants__username= username).count()
        mdsCount = mds.count()
        procentage = "NA"
        if mdsCount > 0:
            procentage = str(count*100/mdsCount) + "%"
        return (str(count) + "/" + str(mdsCount), '<span class="procentage">'+ procentage + '</span>')

register = template.Library()
register.tag('get_atendance_procentage', do_atendance_procentage)

