# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.conf.urls import url
from dolweb.downloads import views

urlpatterns = [
    url(r'^$', views.index, name='downloads_index'),
    url(r'^branches/$', views.branches, name='downloads_branches'),
    url(r'^new/$', views.new, name='downloads_new'),

    url(r'list/(?P<branch>[a-zA-Z0-9_-]+)/(?:(?P<page>\d+)/)?$', views.list, name='downloads_list'),

    url(r'^dev/(?P<hash>[0-9a-f]{40})/$', views.view_dev_release,
        name='downloads_view_devrel'),
    url(r'^dev/(?P<branch>.*?)/(?P<name>.*?)/$', views.view_dev_release_by_name,
        name='downloads_view_devrel_by_name'),

    url(r'^latest/(?P<branch>[a-zA-Z0-9_-]+)/$', views.get_latest, name='downloads_get_latest'),
    url(r'^buildlist$', views.buildlist, name='buildlist_index'),
]
