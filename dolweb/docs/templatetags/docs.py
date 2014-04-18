from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from dolweb.utils.dyni18n import translate, has_translation

import markdown

register = template.Library()

@register.filter
def faq_translate(text):
    return translate('dolweb.docs.faq', text)

@register.filter
def faq_can_translate(text):
    return has_translation('dolweb.docs.faq', text)

@register.filter
@stringfilter
def markdown(text):
    return mark_safe(markdown.markdown(text, safe_mode=True))
