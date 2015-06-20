from annoying.decorators import render_to
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from django.db import models
from django.dispatch import receiver
from django.http import Http404, HttpResponse
from zinnia.managers import PUBLISHED
from zinnia.models.entry import Entry
from django.views.decorators.csrf import csrf_exempt
from zinnia.views.mixins.entry_preview import EntryPreviewMixin

from dolweb.blog.models import BlogSeries

import hashlib
import hmac
import json
import requests
import uuid


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

@csrf_exempt
def etherpad_event(request):
    if request.method != 'POST':
        raise Http404

    if ' ' not in request.body:
        return HttpResponse('Invalid format', status=400)

    request_hmac, content = request.body.split(' ', 1)
    hm = hmac.new(settings.BLOG_ETHERPAD_HMAC_KEY, content, hashlib.sha256)
    if hm.hexdigest() != request_hmac:
        return HttpResponse('Invalid signature', status=403)
    events = json.loads(content)

    last_updates = {}
    for evt in events:
        if evt.get('type') != 'pad_update':
            continue
        last_updates[evt.get('id')] = evt.get('text')

    for pad_id, text in last_updates.iteritems():
        try:
            entry = Entry.objects.get(etherpad_id=pad_id)
            if entry.status == PUBLISHED:
                continue  # Do not auto-sync published articles.
            entry.content = text
            entry.save()
        except Entry.DoesNotExist:
            continue

    return HttpResponse('OK')

# TODO(delroth): Move this to a better place. It cannot be in models.py since
# the Zinnia models depend on importing models.py.
@receiver(models.signals.post_save, sender=Entry)
def add_etherpad_id(sender, instance, created, **kwargs):
    if not settings.BLOG_ETHERPAD_URL or not settings.BLOG_ETHERPAD_API_KEY:
        return
    if instance.etherpad_id:
        return
    instance.etherpad_id = uuid.uuid4()
    url = '%s/api/1/createPad' % settings.BLOG_ETHERPAD_URL
    r = requests.post(url, timeout=5, data={
        'apikey': settings.BLOG_ETHERPAD_API_KEY,
        'padID': instance.etherpad_id,
        'text': instance.content,
    })
    instance.save()
