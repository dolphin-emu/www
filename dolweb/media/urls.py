# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.urls import re_path
from dolweb.media import views

urlpatterns = [
    re_path(r'^$', views.all, name='media_all'),
]
