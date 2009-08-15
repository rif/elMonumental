from django.conf.urls.defaults import *
from news import views
from news.models import News

news_info = {'queryset': News.objects.all()[:5]}

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^$', 'object_list',
        dict(news_info),
        name='news_news_list'),
    url(r'^(?P<slug>[-\w]+)/$',
        'object_detail',
        news_info,
        name='news_news_detail'),
    url(r'^(?(?P<slug>[-\w]+)/rss/$',
        'object_detail',
        dict(news_info, template_name = 'feeds/news_rssdetail.html'),
        name='news_rss_detail'),
)
