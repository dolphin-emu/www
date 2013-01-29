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
        print len(vers)
        vers = vers.filter(title_url__iregex=r'^Ratings/[^a-zA-Z].*$')
        print len(vers)

    vers = vers.select_related('latest__text__data_raw', 'latest__timestamp_raw').order_by('title_url')

    return { 'games': vers, 'pages': ['#'] + list(string.uppercase),
             'page': first_char }
