from django.conf.urls import patterns, url, include
from dolweb.blog.feeds import SeriesFeed

urlpatterns = patterns('',
    url(r'^', include('zinnia.urls')),
    # url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^feeds/series/(?P<pk>[0-9]+)$', SeriesFeed(), name='dolweb_blog_series_feed'),
)

urlpatterns += patterns('dolweb.blog.views',
    # url(r'^series/(?P<slug>[-\w]+)$', 'serie_view'),
    # url(r'^series(/(?P<page>[0-9]+))?$', 'series_index'),
    url(r'^series#series-(?P<uid>[0-9]+)$', 'series_index'),
    url(r'^series$', 'series_index'),
)
