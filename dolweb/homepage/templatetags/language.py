from django import template
from django.conf import settings

register = template.Library()

@register.filter
def langname(lang_code):
    code = lang_code.split('-')[0]
    langs = {}
    for c, n in settings.LANGUAGES:
        langs[c] = n
    return langs.get(code, code)

@register.filter
def short(lang_code):
    return lang_code.split('-')[0]

@register.filter
def to_subdomain(lang_code):
    if lang_code == settings.LANGUAGE_CODE.split('-')[0]:
        return 'dolphin-emu.org'
    else:
        return '%s.dolphin-emu.org' % lang_code
