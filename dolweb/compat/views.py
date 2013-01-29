from annoying.decorators import render_to
from django.views.decorators.cache import cache_page
from dolweb.compat.models import Page, Namespace

import string

@cache_page(60 * 5)
@render_to('compat-list.html')
def list_compat(request, first_char='#'):
    start = 'Ratings/'
    if first_char != '#':
        start += first_char

    vers = (Page.objects.filter(namespace=Namespace.TEMPLATE,
                                title_url__istartswith=start,
                                len=1,
                                latest__text__data_raw__in=('1', '2', '3', '4', '5'))
                        .exclude(title_url='Ratings/'))
    if first_char == '#':
        vers = vers.filter(title_url__iregex=r'^Ratings/[^a-zA-Z].*$')

    vers = vers.select_related('latest__text__data_raw', 'latest__timestamp_raw').order_by('title_url')

    # Re-sort, this time without case taken into account
    vers = list(vers)
    vers.sort(key=lambda v: v.title_url.lower())

    return { 'games': vers, 'pages': ['#'] + list(string.uppercase),
             'page': first_char }
