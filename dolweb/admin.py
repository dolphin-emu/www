# Copyright (c) 2026 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.contrib.admin import AdminSite
from django.contrib.admin.apps import AdminConfig

class DolphinAdminSite(AdminSite):
    enable_nav_sidebar = False

class DolphinAdminConfig(AdminConfig):
    default_site = 'dolweb.admin.DolphinAdminSite'
