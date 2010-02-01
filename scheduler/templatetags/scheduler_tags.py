from django import template
from scheduler.models import MatchDay
import logging

def do_atendance(parser, token):
    return AtendanceNode()

def do_query_matchdays(parser, token):
    return MatchdayQueryNode()

class MatchdayQueryNode(template.Node):
    def render(self, context):
         for sport in (MatchDay.FOOTBALL, MatchDay.VOLLEYBALL, MatchDay.BASKETBALL):
            mds = MatchDay.objects.filter(sport=sport)
            context[sport + '_query'] = mds


class AtendanceNode(template.Node):
    def render(self, context):
        username = context['profile'].user.username
        for sport in (MatchDay.FOOTBALL, MatchDay.VOLLEYBALL, MatchDay.BASKETBALL):
            mds = context[sport + '_query']
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
register.tag('query_matchdays', do_query_matchdays)

