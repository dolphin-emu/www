# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.urls import re_path
from dolweb.docs.views import faq, faq_dyni18n_po, guides_index, guide, privacy

urlpatterns = [
    re_path(r'faq/$', faq, name='docs_faq'),
    re_path(r'faq/template.po$', faq_dyni18n_po, name='docs_faq_dyni18n_po'),
    re_path(r'guides/$', guides_index, name='docs_guides_index'),
    re_path(r'guides/(?P<slug>[\w-]+)/$', guide, name='docs_guide'),
    re_path(r'privacy/$', privacy, name='docs_privacy'),
]
