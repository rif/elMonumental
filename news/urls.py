from django.conf.urls.defaults import *
from news import views
from news.models import News

latest_news = {'queryset': News.objects.all()[:5]}
all_news = {'queryset': News.objects.all()}

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^$',
        'object_list',
        latest_news,
        name='news_news_list'),
    url(r'^(?P<slug>[-\w]+)/$',
        'object_detail',
        all_news,
        name='news_news_detail'),
    url(r'^(?P<slug>[-\w]+)/rss/$',
        'object_detail',
        dict(all_news, template_name = 'feeds/news_rssdetail.html'),
        name='news_rss_detail'),
)
