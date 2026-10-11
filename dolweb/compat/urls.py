# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.urls import re_path
from dolweb.compat.views import list_compat

urlpatterns = [
    re_path(r'^$', list_compat, name='compat_index'),
    re_path(r'^(?:(?P<first_char>[A-Z#])/)?(?:filter/(?P<filter_by>[12345])/)?$', list_compat, name='compat_list'),
]
