from django import template
from django.conf import settings

register = template.Library()

EXCEPTIONS = {
    'pt': ['br'],
    'zh': ['cn'],
}

@register.filter
def short(lang_code):
    parts = lang_code.split('-')
    code = parts[0]
    if code in EXCEPTIONS and len(parts) > 1 and parts[1] in EXCEPTIONS[code]:
        code = parts[1]
    return code

@register.filter
def langname(lang_code):
    code = short(lang_code)
    langs = {}
    for c, n in settings.LANGUAGES:
        langs[c] = n
    return langs.get(code, code)

@register.filter
def to_subdomain(lang_code):
    if lang_code == settings.LANGUAGE_CODE.split('-')[0]:
        return settings.DEFAULT_HOST
    else:
        return '%s.%s' % (lang_code, settings.DEFAULT_HOST)
