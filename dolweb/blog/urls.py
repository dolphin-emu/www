# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.urls import include, re_path
# Load the site's existing preview customization.
from dolweb.blog import views

urlpatterns = [
    re_path(r'^', include('zinnia.urls', namespace='zinnia')),
]
