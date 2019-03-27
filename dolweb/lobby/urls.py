# Copyright (c) 2019 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.conf.urls import url
from dolweb.lobby import views

urlpatterns = [
   # /lobby/v{version}/list/{dolphin_version}/{game_id}/{region}
   url (r'^v(?P<api_ver>\d+)/list?$', views.session_list, name='view_list'),
   # /lobby/v{version}/session/add
   url (r'^v(?P<api_ver>\d+)/session/add?$', views.session_add, name='view_add'),
   # /lobby/v{version}/session/remove
   url (r'^v(?P<api_ver>\d+)/session/remove?$', views.session_remove, name='view_remove'),
   # /lobby/v{version}/session/active
   url (r'^v(?P<api_ver>\d+)/session/active?$', views.session_active, name='view_active'),
]
