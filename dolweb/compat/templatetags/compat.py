from django import template
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from dolweb.compat.models import get_rating_count, get_rated_games

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

@register.filter
def rating_count(compat):
    return get_rating_count(int(compat))

@register.filter
def rating_pct(compat):
    compat = int(compat)
    count = get_rating_count(compat)
    count_all = get_rated_games()
    return (float(count) * 100) / count_all
