from django.conf.urls import patterns, url

urlpatterns = patterns(
    'dolweb.update.views',

    # /update/check/dev/0000000...000
    # /update/check/beta/000000...000
    url(r'^check/v(?P<updater_ver>\d+)/(?P<track>\w+)/(?P<version>[0-9a-f]{40})/?$',
        'check',
        name='update_check'),
)
