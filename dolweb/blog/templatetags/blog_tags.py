from django.template import Library
register = Library()

from dolweb.blog.models import BlogSerie


@register.inclusion_tag('blog_chunk_series.html')
def get_blog_series(number=5):
    """Return the most recent visible blog series"""
    return {
        'series': BlogSerie.objects.filter(visible=True)[:number],
    }
