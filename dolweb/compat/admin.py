# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.contrib import admin
from dolweb.compat.models import Page, Revision, Category, CategoryLink


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'namespace')
    ordering = ('namespace', 'title_url')
admin.site.register(Page, PageAdmin)

class RevisionAdmin(admin.ModelAdmin):
    list_display = ('page', 'text', 'timestamp')
    ordering = ('timestamp',)
admin.site.register(Revision, RevisionAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ('id',)
admin.site.register(Category, CategoryAdmin)

class CategoryLinkAdmin(admin.ModelAdmin):
    list_display = ('page', 'cat')
admin.site.register(CategoryLink, CategoryLinkAdmin)
