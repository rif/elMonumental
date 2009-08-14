from django.conf.urls.defaults import *
from scheduler import views
from models import News

news_info = {'queryset': News.objects.all()}

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^$', 'object_list',
        dict(news_info, paginate_by = 10),
        name='news_news_list'),
    url(r'^news/(?P<object_id>\w+)/$',
        'object_detail',
        news_info,
        name='news_news_detail'),
)
