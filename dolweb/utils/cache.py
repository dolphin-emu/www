# Copyright (c) 2019 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.views.decorators.cache import patch_cache_control
from django.utils.cache import patch_response_headers


class DefaultCacheControlMiddleware:
    """Used to set a default Cache-Control header."""
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        if response.get('Cache-Control'):
            return response
        if response.status_code != 200:
            return response

        if request.user.is_authenticated:
            patch_cache_control(response, private=True)
        else:
            patch_cache_control(response, public=True)
            patch_response_headers(response, 300)
        return response
