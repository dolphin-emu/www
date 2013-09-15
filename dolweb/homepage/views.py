from annoying.decorators import render_to
from django.conf import settings
from dolweb.downloads.models import DevVersion, ReleaseVersion
from dolweb.homepage.models import NewsArticle
from dolweb.media.models import Screenshot
from zinnia.models import Entry

import random


@render_to('homepage-home.html')
def home(request):
    featured = list(Screenshot.objects.filter(promoted=True).order_by('game_name'))
    random.shuffle(featured)
    featured = featured[:6]
    try:
        last_release = ReleaseVersion.objects.order_by('-date')[0]
    except IndexError:
        last_release = u"Dolphin"
    last_master = DevVersion.objects.filter(branch='master').order_by('-date')[0]

    home_articles = Entry.published.all()[:settings.HOMEPAGE_ARTICLES]

    return { 'featured_images': featured, 'last_release': last_release,
             'last_master': last_master, 'all_ratings': (5, 4, 3, 2, 1),
             'home_articles': home_articles }
