from django.conf import settings

def website_urls(request):
    return {
        "FORUM_URL": settings.FORUM_URL,
        "WIKI_URL": settings.WIKI_URL,
        "GIT_BROWSE_URL": settings.GIT_BROWSE_URL,
        "GIT_CLONE_URL": settings.GIT_CLONE_URL,
        "GIT_COMMIT_URL": settings.GIT_COMMIT_URL,
        "WEBSITE_GIT_URL": settings.WEBSITE_GIT_URL,
        "ISSUES_URL": settings.ISSUES_URL,
        "GOOGLE_ANALYTICS_ACCOUNT": settings.GOOGLE_ANALYTICS_ACCOUNT,
        "DEFAULT_HOST": settings.DEFAULT_HOST,
    }

def guess_system_from_ua(request):
    ua = request.META.get('HTTP_USER_AGENT', None)
    if ua is None:
        return { "USER_OS": "unknown" }

    if "Windows" in ua:
        return { "USER_OS": "win" }
    elif "Macintosh" in ua:
        return { "USER_OS": "osx" }
    elif "Ubuntu" in ua:
        return { "USER_OS": "ubu" }
    elif "Android" in ua:
        return { "USER_OS": "android" }
    else:
        return { "USER_OS": "unknown" }

def check_country_redirect(request):
    if request.GET.get('cr'):
        return { "COUNTRY_REDIRECT": request.GET['cr'] }
    return {}

def export_languages(request):
    return {
        "LANGUAGES": settings.LANGUAGES,
        "LANGUAGE_CODE": settings.LANGUAGE_CODE,
    }
