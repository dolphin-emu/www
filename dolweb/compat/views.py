from annoying.decorators import render_to
from django.views.decorators.cache import cache_page
from dolweb.compat.models import Page, Namespace, get_category_id, \
                                 CategoryLink

import hashlib
import string

CATEGORIES = {
    'GameCube_games': 'gamecube',
    'Wii_games': 'wii',
    'WiiWare_games': 'wiiware',
    'Wii_Channels': 'channel',
    'Virtual_Console_games': 'virtual-console',
}

@cache_page(60 * 5)
@render_to('compat-list.html')
def list_compat(request, first_char='#'):
    ratings_start = 'Ratings/'
    gpages_start = ''
    if first_char != '#':
        ratings_start += first_char
        gpages_start += first_char

    # Select all the relevant ratings pages
    ratings = (Page.objects.filter(namespace=Namespace.TEMPLATE,
                                   title_url__istartswith=ratings_start,
                                   len=1,
                                   latest__text__data_raw__in=('1', '2', '3', '4', '5'))
                           .exclude(title_url='Ratings/'))
    if first_char == '#':
        ratings = ratings.filter(title_url__iregex=r'^Ratings/[^a-zA-Z].*$')
    ratings = ratings.select_related('latest__text__data_raw', 'latest__timestamp_raw').order_by('title_url')

    # Re-sort ratings, this time without case taken into account
    ratings = list(ratings)
    ratings.sort(key=lambda v: v.title_url.lower())

    # Then select all the relevant game pages, maybe with some false-positives.
    # Query the category links at the same time to avoid having one query per row.
    categories = CategoryLink.objects.filter(cat__in=CATEGORIES.keys(),
                                             page__namespace=Namespace.MAIN,
                                             page__title_url__istartswith=gpages_start)
    if first_char == '#':
        categories = categories.filter(page__title_url__iregex=r'^[^a-zA-Z].*$')
    categories = categories.select_related('page__title_url', 'page__latest__timestamp_raw')

    # Make a categories dict using the titles
    cat_dict = {}
    for c in categories:
        cat_dict[c.page.title_url] = c

    # Group ratings with their associated categories.
    games = []
    for rating in ratings:
        title = rating.title_url[len('Ratings/'):]
        if title in cat_dict:
            hash = hashlib.sha1(title).hexdigest()[:8]
            ts = max(rating.latest.timestamp, cat_dict[title].page.latest.timestamp)
            games.append((rating, CATEGORIES[cat_dict[title].cat], ts, hash))

    return { 'games': games, 'pages': ['#'] + list(string.uppercase),
            'page': first_char, 'page_css': first_char.replace('#', '%23'),
            'all_ratings': (5, 4, 3, 2, 1) }
