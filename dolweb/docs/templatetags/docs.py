import markdown

from django import template
from django.utils import safestring
from dolweb.utils.dyni18n import translate, has_translation

register = template.Library()

@register.filter
def faq_translate(text):
    return translate('dolweb.docs.faq', text)

@register.filter
def faq_can_translate(text):
    return has_translation('dolweb.docs.faq', text)

@register.filter
def faq_markdown(text):
    return safestring.mark_safe(markdown.markdown(text))
