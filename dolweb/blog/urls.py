from django.conf.urls import patterns, url, include
from dolweb.blog.feeds import SerieFeed

urlpatterns = patterns('',
    url(r'^', include('zinnia.urls', namespace='zinnia')),
    # url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^feeds/serie/(?P<pk>[0-9]+)$', SerieFeed(), name='dolweb_blog_serie_feed'),
)

urlpatterns += patterns('dolweb.blog.views',
    # url(r'^series/(?P<slug>[-\w]+)$', 'serie_view'),
    # url(r'^series(/(?P<page>[0-9]+))?$', 'series_index'),
    url(r'^series#serie-(?P<uid>[0-9]+)$', 'series_index'),
    url(r'^series$', 'series_index'),
)
