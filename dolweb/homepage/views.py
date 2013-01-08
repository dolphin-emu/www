from annoying.decorators import render_to
from dolweb.downloads.models import ReleaseVersion
from dolweb.homepage.models import NewsArticle
from dolweb.media.models import Screenshot

@render_to('homepage-home.html')
def home(request):
    featured = Screenshot.objects.filter(promoted=True).order_by('game_name')
    news = NewsArticle.objects.filter(published=True).order_by('-posted_on')[:4]
    try:
        last_release = ReleaseVersion.objects.order_by('-date')[0]
    except IndexError:
        last_release = u"Dolphin"
    return { 'featured_images': featured, 'last_release': last_release,
             'latest_news': news }
