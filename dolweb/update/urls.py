# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.conf.urls import url
from dolweb.update import views

urlpatterns = [
    # /update/latest/beta/
    url(r'^latest/(?P<track>\w+)/?$', views.latest, name='update_latest'),

    # /update/check/v1/dev/0000000000000000000000000000000000000000/win
    # /update/check/v1/beta/0000000000000000000000000000000000000000/win
    url(r'^check/v(?P<updater_ver>\d+)/(?P<track>\w+)/(?P<version>[0-9a-f]{40})/?(?P<platform>[A-Za-z0-9-_]+)?$',
        views.check,
        name='update_check'),

    # /update/info/v1/0000000000000000000000000000000000000000/win
    url(r'^info/v(?P<updater_ver>\d+)/(?P<version>[0-9a-f]{40})/?(?P<platform>[A-Za-z0-9-_]+)?$',
        views.info,
        name='update_info'),
]
