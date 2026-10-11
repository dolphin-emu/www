# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.conf import settings
from django.urls import include, re_path
from dolweb.blog.feeds import SeriesFeed
from dolweb.blog.views import series_index, etherpad_event

urlpatterns = [
    re_path(r'^', include('zinnia.urls', namespace='zinnia')),
    re_path(r'^feeds/series/(?P<pk>[0-9]+)$', SeriesFeed(), name='dolweb_blog_series_feed'),
    re_path(r'^series#series-(?P<uid>[0-9]+)$', series_index, name='dolweb_blog_series'),
    re_path(r'^series$', series_index, name='dolweb_blog_series_index'),
]

if settings.BLOG_ETHERPAD_URL:
    urlpatterns += [
        re_path(r'^etherpad/event$', etherpad_event),
    ]
