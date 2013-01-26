from django.conf.urls import patterns, url

urlpatterns = patterns('dolweb.downloads.views',
    url(r'^$', 'index', name='downloads-index'),
    url(r'^branches/$', 'branches', name='downloads-branches'),
    url(r'^new/$', 'new', name='downloads-new'),

    url(r'list/(?P<branch>[a-zA-Z0-9_-]+)/(?P<page>\d+)/$', 'list', name='downloads-list'),

    url(r'^dev/(?P<hash>[0-9a-f]{40})/$', 'view_dev_release',
        name='downloads-view-devrel'),

    url(r'^latest/(?P<branch>[a-zA-Z0-9_-]+)/$', 'get_latest', name='downloads-get-latest'),
)
