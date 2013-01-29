from django.contrib import admin
from dolweb.compat.models import Page

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'namespace')
    ordering = ('namespace', 'title_url')
admin.site.register(Page, PageAdmin)
