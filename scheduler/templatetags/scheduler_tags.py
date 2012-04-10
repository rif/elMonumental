from django import template

register = template.Library()

@register.tag
def get_attendance(parser, token):
    return AttendanceNode()

@register.filter
def attendance(value, arg):
    return value[arg][0]

@register.filter
def procentage(value, arg):
    return value[arg][1]

""" Depends on MatchdayQueryNode being executed for efficiency """
class AttendanceNode(template.Node):
    def render(self, context):
        username = context['profile'].user.username
        result_dict = {}
        for sport in context['sport_list']:
            mdsCount = sport.matchday_sport__count
            count = sport.matchday_sport.filter(participants__username=username).count()
            procentage = "NA"
            if mdsCount > 0: procentage = str(count*100/mdsCount) + "%"
            result_dict[sport] = (str(count) + "/" + str(mdsCount), procentage)
        context['attendance_dict'] = result_dict
        return ''
