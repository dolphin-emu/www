from django.conf.urls import patterns, url

urlpatterns = patterns('dolweb.downloads.views',
    url(r'^$', 'index', name='downloads_index'),
    url(r'^branches/$', 'branches', name='downloads_branches'),
    url(r'^new/$', 'new', name='downloads_new'),

    url(r'list/(?P<branch>[a-zA-Z0-9_-]+)/(?:(?P<page>\d+)/)?$', 'list', name='downloads_list'),

    url(r'^dev/(?P<hash>[0-9a-f]{40})/$', 'view_dev_release',
        name='downloads_view_devrel'),
    url(r'^dev/(?P<branch>.*?)/(?P<name>.*?)/$', 'view_dev_release_by_name',
        name='downloads_view_devrel_by_name'),

    url(r'^latest/(?P<branch>[a-zA-Z0-9_-]+)/$', 'get_latest', name='downloads_get_latest'),
)
