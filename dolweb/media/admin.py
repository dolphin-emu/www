from django.contrib import admin
from dolweb.media.models import Screenshot

class ScreenshotAdmin(admin.ModelAdmin):
    list_display = ('game_name', 'image', 'displayed', 'promoted')
    list_filter = ('displayed', 'promoted')
    ordering = ('-displayed', '-promoted', 'game_name')
admin.site.register(Screenshot, ScreenshotAdmin)
