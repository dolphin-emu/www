# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.conf.urls import url
from dolweb.docs.views import faq, faq_dyni18n_po, guides_index, guide

urlpatterns = [
    url(r'faq/$', faq, name='docs_faq'),
    url(r'faq/template.po$', faq_dyni18n_po, name='docs_faq_dyni18n_po'),
    url(r'guides/$', guides_index, name='docs_guides_index'),
    url(r'guides/(?P<slug>[\w-]+)/$', guide, name='docs_guide'),
]
