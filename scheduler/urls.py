from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'elMonumental.scheduler.views.index'),
)
