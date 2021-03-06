from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('scheduler.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^profiles/', include('profiles.urls')),
    (r'^news/', include('news.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^forum/', include('forum.urls')),
)
# if we're in DEBUG mode, allow django to serve media
# This is considered inefficient and isn't secure.
from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
