from annoying.decorators import render_to
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from zinnia.views.mixins.entry_preview import EntryPreviewMixin

from dolweb.blog.models import BlogSeries


@render_to('series-index.html')
def series_index(request, page=None):
    all_series = BlogSeries.objects.filter(visible=True)

    # if page is None:
    #     page = 1

    # pagi = Paginator(series, 20)

    # try:
    #     page_obj = pagi.page(page)
    # except EmptyPage:
    #     raise Http404

    # return {'page': page, 'page_obj': page_obj, 'pagi': pagi}
    return {'all_series': all_series}


# @render_to('serie-view.html')
# def serie_view(request, uid=None, slug=None):
#     both = (uid, slug)
#     if not any(both) or all(both):
#         raise Http404
#
#     if uid is not None:
#         serie = get_object_or_404(BlogSerie, pk=uid)
#     else:
#         serie = get_object_or_404(BlogSerie, slug=slug)
#
#     return {'serie': serie}

# TODO(delroth): Ugly. Should really authenticate these requests, but we don't
# have a nice SSO story at the moment.
del EntryPreviewMixin.get_object
