from annoying.decorators import render_to
from dolweb.media.models import Screenshot

@render_to('media-all.html')
def all(request):
    images = Screenshot.objects.filter(displayed=True).order_by('game_name')
    return { 'images': images }
