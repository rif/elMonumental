from django import template
from scheduler.models import MatchDay
import logging

def do_atendance(parser, token):
    return AtendanceNode()

class AtendanceNode(template.Node):
    def render(self, context):        
        username = context['profile'].user.username        
        for sport in (MatchDay.FOOTBALL, MatchDay.VOLLEYBALL, MatchDay.BASKETBALL):
            mds = MatchDay.objects.filter(sport=sport)
            mdsCount = mds.count()
            count = mds.filter(participants__username=username).count()                
            procentage = "NA"
            if mdsCount > 0:
                procentage = str(count*100/mdsCount) + "%"         
            context[sport + '_count'] = str(count) + "/" + str(mdsCount)
            context[sport + '_procentage'] = procentage
        return ''

register = template.Library()
register.tag('get_atendance', do_atendance)

