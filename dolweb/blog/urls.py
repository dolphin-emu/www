# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.conf import settings
from django.urls import include, re_path
from dolweb.blog.views import etherpad_event

urlpatterns = [
    re_path(r'^', include('zinnia.urls', namespace='zinnia')),
]

if settings.BLOG_ETHERPAD_URL:
    urlpatterns += [
        re_path(r'^etherpad/event$', etherpad_event),
    ]
