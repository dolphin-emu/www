from django import template
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
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
    if count_all == 0:
        return 0
    return (float(count) * 100) / count_all

@register.filter
def rating_class(compat):
    return {
        0: 'danger',
        1: 'danger',
        2: 'danger',
        3: 'warning',
        4: 'success',
        5: 'info',
    }[int(compat)]

@register.simple_tag
def platform_img_url(platform):
    return staticfiles_storage.url(u'img/platforms/%s.png' % unicode(platform))

@register.simple_tag
def compat_img_url(compat):
    return staticfiles_storage.url(u'img/stars/%s.png' % unicode(compat))

@register.simple_tag
def compat_url(char, rating):
    kwargs = {}
    if rating:
        kwargs['filter_by'] = rating
    if char and char != '#':
        kwargs['first_char'] = char
    return reverse('compat_list', kwargs=kwargs)
