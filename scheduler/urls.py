from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', include('elMonumental.scheduler.views.index')),
)
