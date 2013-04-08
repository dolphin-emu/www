from annoying.decorators import render_to
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from dolweb.docs.models import FAQCategory, FAQ, Guide

import polib
import requests

@render_to('docs-faq.html')
def faq(request):
    categories = FAQCategory.objects.order_by('display_order')
    categories = categories.prefetch_related('questions')

    return { 'categories': categories }

@render_to('docs-guides-index.html')
def guides_index(request):
    guides = Guide.objects.filter(listed=True).order_by('display_order', 'title')
    return { 'guides': guides }

@cache_page(60 * 5)
@render_to('docs-guide.html')
def guide(request, slug):
    guide = get_object_or_404(Guide, slug=slug)
    html = requests.get(guide.get_wiki_url()).text

    # Hack to rebase the URLs
    html = html.replace('src="/', 'src="http://wiki.dolphin-emu.org/')
    html = html.replace('href="/', 'href="http://wiki.dolphin-emu.org/')

    return { 'title': guide.title, 'guide': html }

def faq_dyni18n_po(request):
    po = polib.POFile()
    po.metadata = {
        'Project-Id-Version': '1.0',
        'Report-Msgid-Bugs-To': 'contact@dolphin-emu.org',
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Transfer-Encoding': '8bit',
    }

    for cat in FAQCategory.objects.order_by('display_order'):
        po.append(polib.POEntry(msgid=cat.title, msgstr=u'', msgctxt=u'Category title'))
        for q in cat.sorted_questions():
            po.append(polib.POEntry(msgid=q.title, msgstr=u'', msgctxt=u'Question title'))
            po.append(polib.POEntry(msgid=q.short_title, msgstr=u'',
                                    msgctxt=u'Question short title (displayed in the left column)'))
            po.append(polib.POEntry(msgid=q.text, msgstr=u'', msgctxt=u'Answer'))
    return HttpResponse(unicode(po))
