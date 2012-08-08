from django.conf.urls import patterns, url

urlpatterns = patterns('dolweb.media.views',
    url(r'^$', 'all', name='media-all'),
)
