from annoying.decorators import render_to
from django.template import RequestContext

@render_to('homepage-home.html')
def home(request):
    return {}

def news_article(request):
    raise NotImplemented
