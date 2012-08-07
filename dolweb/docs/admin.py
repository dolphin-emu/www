from django.contrib import admin
from dolweb.docs.models import FAQ, Guide

class FAQAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'last_updated')
    ordering = ('category', 'title')
    prepopulated_fields = { 'slug': ('title',) }
admin.site.register(FAQ, FAQAdmin)

class GuideAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'last_updated', 'published')
    list_filter = ('published',)
    ordering = ('-published', 'title')
    prepopulated_fields = { 'slug': ('title',) }
admin.site.register(Guide, GuideAdmin)
