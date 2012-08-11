from django.conf import settings

def website_urls(request):
    return {
        "FORUM_URL": settings.FORUM_URL,
        "WIKI_URL": settings.WIKI_URL,
        "GCODE_URL": settings.GCODE_URL,
        "GOOGLE_ANALYTICS_ACCOUNT": settings.GOOGLE_ANALYTICS_ACCOUNT,
    }

def guess_system_from_ua(request):
    ua = request.META.get('HTTP_USER_AGENT', None)
    if ua is None:
        return { "USER_OS": "unknown" }

    if "Windows" in ua:
        return { "USER_OS": "win" }
    elif "Macintosh" in ua:
        return { "USER_OS": "osx" }
    else:
        return { "USER_OS": "unknown" }
