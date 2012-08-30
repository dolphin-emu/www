from annoying.decorators import render_to
from dolweb.downloads.models import ReleaseVersion
from dolweb.media.models import Screenshot

@render_to('homepage-home.html')
def home(request):
    featured = Screenshot.objects.filter(promoted=True).order_by('game_name')
    try:
        last_release = ReleaseVersion.objects.order_by('-date')[0]
    except IndexError:
        last_release = u"Dolphin"
    return { 'featured_images': featured, 'last_release': last_release }

def news_article(request):
    raise NotImplemented
