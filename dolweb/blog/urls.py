# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.urls import include, re_path

urlpatterns = [
    re_path(r'^', include('zinnia.urls', namespace='zinnia')),
]
