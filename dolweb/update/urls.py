# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.urls import re_path
from dolweb.update import views

urlpatterns = [
    # /update/latest/beta/
    re_path(r'^latest/(?P<track>\w+)/?$', views.latest, name='update_latest'),

    # /update/check/v1/dev/0000000000000000000000000000000000000000/win
    # /update/check/v1/beta/0000000000000000000000000000000000000000/win
    re_path(r'^check/v(?P<updater_ver>\d+)/(?P<track>\w+)/(?P<version>[0-9a-f]{40})/?(?P<platform>[A-Za-z0-9-_]+)?$',
        views.check,
        name='update_check'),

    # /update/info/v1/0000000000000000000000000000000000000000/win
    re_path(r'^info/v(?P<updater_ver>\d+)/(?P<version>[0-9a-f]{40})/?(?P<platform>[A-Za-z0-9-_]+)?$',
        views.info,
        name='update_info'),

    # /update/obtainium/
    re_path(r'^obtainium/?$', views.obtainium, name='update_obtainium'),
]
