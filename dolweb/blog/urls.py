from django.conf import settings
from django.conf.urls import url, include
from dolweb.blog.feeds import SeriesFeed
from dolweb.blog.views import series_index, etherpad_event

urlpatterns = [
    url(r'^', include('zinnia.urls', namespace='zinnia')),
    url(r'^feeds/series/(?P<pk>[0-9]+)$', SeriesFeed(), name='dolweb_blog_series_feed'),
    url(r'^series#series-(?P<uid>[0-9]+)$', series_index, name='dolweb_blog_series'),
    url(r'^series$', series_index, name='dolweb_blog_series_index'),
]

if settings.BLOG_ETHERPAD_URL:
    urlpatterns += [
        url(r'^etherpad/event$', etherpad_event),
    ]
