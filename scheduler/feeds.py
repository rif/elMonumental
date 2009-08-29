from django.contrib.syndication.feeds import Feed
from scheduler.models import MatchDay
from news.models import News

class LatestMatchDays(Feed):
    title = "elMonumental"
    link = '/'
    description = "Updates on changes and additions to elMonumental."

    def items(self):
        return MatchDay.objects.order_by('-start_date')[:5]

    def item_link(self, item):
        return '/matchday/' + str(item.id) + '/rss/'
    
    def item_categories(self, item):
        return [c[1] for c in item.SPORT_CHOICES]

class LatestNews(Feed):
    title = "elMonumental news"
    link = "/news/"
    description = "Latest news about football and elMonumental."
    
    def items(self):
        return News.objects.order_by('-pub_date')[:5]

    def item_link(self, item):
        return '/news/' + str(item.slug) + '/rss/'
