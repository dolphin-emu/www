from annoying.decorators import render_to
from django.views.decorators.cache import cache_page
from dolweb.media.models import Screenshot

@cache_page(60 * 5)
@render_to('media-all.html')
def all(request):
    images = Screenshot.objects.filter(displayed=True).order_by('game_name')
    return { 'images': images }
