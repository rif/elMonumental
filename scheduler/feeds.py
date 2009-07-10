from django.contrib.syndication.feeds import Feed
from models import MatchDay

class LatestMatchDays(Feed):
    title = "elMonumental"
    link = '/'
    description = "Updates on changes and additions to elMonumental."

    def items(self):
        return MatchDay.objects.order_by('-start_date')[:5]

    def item_link(self, item):
        return '/matchday/' + str(item.id) + '/rss/'
