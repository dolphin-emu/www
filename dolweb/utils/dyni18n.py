# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.conf import settings
from django.utils.translation import get_language

import glob
import os.path
import polib
import time

UPDATE_EVERY = 300

_DOMAINS = {}

class DynI18NDomain(object):
    def __init__(self, name):
        self.name = name
        self.last_update = 0
        self.strings = {}
        self.update(force=True)

    def update(self, force=False):
        if not force and time.time() - self.last_update < UPDATE_EVERY:
            return

        pattern = os.path.join(settings.DYNI18N_PATH, '%s.*.po' % self.name)
        files = glob.glob(pattern)

        self.strings = {}
        for file in files:
            lang = file.split('.')[-2]
            self.strings[lang] = {}

            po = polib.pofile(file)
            for entry in po.translated_entries():
                self.strings[lang][entry.msgid] = entry.msgstr

        self.last_update = time.time()

    def language_to_key(self, lang):
        if '-' in lang:
            l1, l2 = lang.split('-', 1)
            lang = l1 + '_' + l2.upper()
        if lang in self.strings:
            return lang
        elif lang.split('_')[0] in self.strings:
            return lang.split('_')[0]
        else:
            return lang

    def translate(self, string):
        self.update()
        lang = self.language_to_key(get_language())
        if lang not in self.strings:
            return string
        if string not in self.strings[lang]:
            return string
        return self.strings[lang][string]

    def has_translation(self, string):
        self.update()
        lang = self.language_to_key(get_language())
        if lang not in self.strings:
            return False
        if string not in self.strings[lang]:
            return False
        return True

def get_or_create_domain(domain):
    if domain in _DOMAINS:
        return _DOMAINS[domain]

    obj = DynI18NDomain(domain)
    _DOMAINS[domain] = obj
    return obj

def translate(domain, string):
    domain = get_or_create_domain(domain)
    return domain.translate(string)

def has_translation(domain, string):
    domain = get_or_create_domain(domain)
    return domain.has_translation(string)
