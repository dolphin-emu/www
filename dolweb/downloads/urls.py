from django.conf.urls import patterns, url

urlpatterns = patterns('dolweb.downloads.views',
    url(r'^$', 'index', name='downloads-index'),
    url(r'^branches/$', 'branches', name='downloads-branches'),
    url(r'^new/$', 'new', name='downloads-new'),

    url(r'^dev/(?P<hash>[0-9a-f]{40})/$', 'view_dev_release',
        name='downloads-view-devrel'),
)
