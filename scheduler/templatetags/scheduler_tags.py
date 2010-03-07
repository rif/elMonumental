from django import template
from scheduler.models import MatchDay, Sport
import logging

register = template.Library()

@register.tag('get_attendance')
def do_attendance(parser, token):
    return AttendanceNode()

@register.tag('query_matchdays')
def do_query_matchdays(parser, token):
    return MatchdayQueryNode()

@register.filter
def attendance(value, arg):
    return value[arg][0]

@register.filter
def procentage(value, arg):
    return value[arg][1]

class MatchdayQueryNode(template.Node):
    def render(self, context):
        for sport in context['sport_list']:
            mds = MatchDay.objects.filter(sport_name=sport)
            context[sport.name + '_query'] = mds
            context[sport.name + '_counter'] = mds.count()
        return ''

""" Depends on MatchdayQueryNode being executed for efficiency """
class AttendanceNode(template.Node):
    def render(self, context):
        username = context['profile'].user.username
        result_dict = {}
        for sport in context['sport_list']:
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
            result_dict[sport] = (str(count) + "/" + str(mdsCount), procentage)
        context['attendance_dict'] = result_dict
        return ''
