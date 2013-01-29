from django.conf.urls import patterns, url

urlpatterns = patterns('dolweb.compat.views',
    url(r'^(?P<page>\d+)/$', 'list', name='compat-list'),
)
