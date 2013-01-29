from annoying.decorators import render_to
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from dolweb.compat.models import Page, Namespace

@render_to('compat-list.html')
def list(request, page):
    vers = (Page.objects.filter(namespace=Namespace.TEMPLATE,
                                title_url__startswith='Ratings/',
                                len=1,
                                latest__text__data_raw__in=('1', '2', '3', '4', '5'))
                        .exclude(title_url='Ratings/')
                        .select_related('latest__text__data_raw',
                                        'latest__timestamp_raw')
                        .order_by('title_url'))
    pagi = Paginator(vers, 100)

    try:
        page_obj = pagi.page(page)
    except EmptyPage:
        raise Http404

    return { 'page': page, 'page_obj': page_obj, 'pagi': pagi }
