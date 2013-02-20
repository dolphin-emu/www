from django import template
from dolweb.utils.dyni18n import translate

register = template.Library()

@register.filter
def faq_translate(text):
    return translate('dolweb.docs.faq', text)
