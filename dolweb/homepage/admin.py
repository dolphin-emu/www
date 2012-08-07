from django.contrib import admin
from dolweb.homepage.models import Screenshot, NewsArticle

class ScreenshotAdmin(admin.ModelAdmin):
    list_display = ('game_name', 'image', 'published')
    list_filter = ('published',)
    ordering = ('-published', 'game_name')
admin.site.register(Screenshot, ScreenshotAdmin)

class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'posted_on', 'published')
    list_filter = ('published',)
    ordering = ('-posted_on',)
    prepopulated_fields = { 'slug': ('title',) }
admin.site.register(NewsArticle, NewsArticleAdmin)
