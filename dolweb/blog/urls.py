from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^', include('zinnia.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
)

urlpatterns += patterns('dolweb.blog.views',
    # url(r'^series/(?P<slug>[-\w]+)$', 'serie_view'),
    # url(r'^series/(?P<uid>[0-9]+)$', 'serie_view'),
    url(r'^series(/(?P<page>[0-9]+))?$', 'series_index'),
)
