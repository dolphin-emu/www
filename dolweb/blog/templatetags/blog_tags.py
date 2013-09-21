from django.template import Library
register = Library()

from bs4 import BeautifulSoup
from django.conf import settings
from django.template import defaultfilters
from dolweb.blog.models import BlogSerie

@register.inclusion_tag('blog_chunk_series.html')
def get_blog_series(number=5):
    """Return the most recent visible blog series"""
    return {
        'series': BlogSerie.objects.filter(visible=True)[:number],
    }


@register.filter
def cuthere_excerpt(content):
    try:
        cut_here = BeautifulSoup(content).find('a', id='cuthere')
        return ''.join(map(str, reversed(cut_here.parent.find_previous_siblings())))
    except AttributeError:
        return defaultfilters.truncatewords(content, 100)
