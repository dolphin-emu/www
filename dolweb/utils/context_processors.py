from django.conf import settings

def website_urls(request):
    return {
        "FORUM_URL": settings.FORUM_URL,
        "WIKI_URL": settings.WIKI_URL,
        "GCODE_URL": settings.GCODE_URL,
    }
