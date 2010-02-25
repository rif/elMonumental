from django import template
from scheduler.models import MatchDay, Sport
import logging

def do_atendance(parser, token):
    return AtendanceNode()

def do_query_matchdays(parser, token):
    return MatchdayQueryNode()

class MatchdayQueryNode(template.Node):
    def render(self, context):
        for sport in Sport.objects.iterator():
            mds = MatchDay.objects.filter(sport_name=sport)
            context[sport.name + '_query'] = mds
            context[sport.name + '_counter'] = mds.count()
        return ''


class AtendanceNode(template.Node):
    def render(self, context):
        username = context['profile'].user.username
        result_dict = {}
        for sport in Sport.objects.iterator():
            mds = context[sport.name + '_query']
            mdsCount = context[sport.name + '_counter']
            if context.has_key('since'):
                mds = mds.filter(start_date__gte=context['since'])
                mdsCount =  mds.count()
            count = mds.filter(participants__username=username).count()
            procentage = "NA"
            if mdsCount > 0:
                procentage = str(count*100/mdsCount) + "%"
#            context[sport.name + '_count'] = str(count) + "/" + str(mdsCount)
#            context[sport.name + '_procentage'] = procentage
            result_dict[sport.name] = (str(count) + "/" + str(mdsCount), procentage)
        context['atendance_dict'] = result_dict
        logging.debug(result_dict)
        return ''

register = template.Library()
register.tag('get_atendance', do_atendance)
register.tag('query_matchdays', do_query_matchdays)

