from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.translation.trans_real import parse_accept_lang_header
from dolweb.utils.monkey import TO_FULL_INVERTED

import datetime

def guess_lang_from_request(request):
    if request.GET.get('nocr'):
        return

    if request.META.get('HTTP_HOST', settings.DEFAULT_HOST) != settings.DEFAULT_HOST:
        return # Do not guess if we are on a lang subdomain

    no_guess_please = request.COOKIES.get("no_country_redirect")
    if no_guess_please is not None:
        return # Do not guess if a cookie is present

    accept = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    for accept_lang, unused in parse_accept_lang_header(accept):
        normalized_accept_lang = accept_lang.lower().replace('-', '_')
        if normalized_accept_lang in TO_FULL_INVERTED:
            return TO_FULL_INVERTED[normalized_accept_lang]

        if '_' in normalized_accept_lang:
            normalized_accept_lang = normalized_accept_lang.split('_')[0]

        if normalized_accept_lang == settings.LANGUAGE_CODE.split('-')[0]:
            break

        if normalized_accept_lang in dict(settings.LANGUAGES):
            return normalized_accept_lang

class CountryRedirectMiddleware(object):
    def process_request(self, request):
        guess = guess_lang_from_request(request)
        if guess is None:
            return

        return HttpResponseRedirect("http://%s.%s%s?cr=%s" % (guess, settings.DEFAULT_HOST, request.path, guess))

    def process_response(self, request, response):
        if request.GET.get('nocr'):
            expires = datetime.datetime.now() + datetime.timedelta(seconds=3600 * 24 * 365)
            response.set_cookie('no_country_redirect', expires=expires)
        return response
