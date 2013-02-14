from django import template
from django.conf import settings

from django.utils.translation import ugettext_lazy as _

COMPAT_TEXTS = {
    0: _('Unknown'),
    1: _('Broken'),
    2: _('Intro/Menu'),
    3: _('Starts'),
    4: _('Playable'),
    5: _('Perfect'),
}

register = template.Library()

@register.filter
def compat_text(compat):
    return COMPAT_TEXTS[int(compat)]
