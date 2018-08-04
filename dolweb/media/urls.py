# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.conf.urls import url
from dolweb.media import views

urlpatterns = [
    url(r'^$', views.all, name='media_all'),
]
