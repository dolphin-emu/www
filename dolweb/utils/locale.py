# Copyright (c) 2026 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.conf import settings
from django.middleware.locale import LocaleMiddleware
from django.utils import translation


TO_FULL = {
    'br': 'pt-BR',
    'cn': 'zh-CN',
    'ms': 'ms-MY',
}
TO_FULL_INVERTED = {v.lower(): k for k, v in TO_FULL.items()}


def language_from_host(request):
    code = request.get_host().split('.')[0]
    language = TO_FULL.get(code, code)
    if code in dict(settings.LANGUAGES) and translation.check_for_language(language):
        return language
    return settings.LANGUAGE_CODE


class HostLocaleMiddleware(LocaleMiddleware):
    """Select translations from the language subdomain."""

    def process_request(self, request):
        translation.activate(language_from_host(request))
        request.LANGUAGE_CODE = translation.get_language()
