# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.contrib import admin
from dolweb.blog.models import ForumThreadForEntry


class ForumThreadForEntryAdmin(admin.ModelAdmin):
    pass


admin.site.register(ForumThreadForEntry, ForumThreadForEntryAdmin)
