from annoying.decorators import render_to
from dolweb.media.models import Screenshot

@render_to('homepage-home.html')
def home(request):
    return { 'featured_images': Screenshot.objects.filter(promoted=True).order_by('game_name') }

def news_article(request):
    raise NotImplemented
