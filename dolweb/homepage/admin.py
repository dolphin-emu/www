# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.contrib import admin
from dolweb.homepage.models import NewsArticle

class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'posted_on', 'published')
    list_filter = ('published',)
    ordering = ('-posted_on',)
    prepopulated_fields = { 'slug': ('title',) }
admin.site.register(NewsArticle, NewsArticleAdmin)
