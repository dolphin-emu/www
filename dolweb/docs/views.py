from annoying.decorators import render_to
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from dolweb.docs.models import FAQCategory, FAQ, Guide

import polib
import re
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
    headers = { 'X-Forwarded-Proto': 'https' }  # cheat!
    html = requests.get(guide.get_wiki_url(), headers=headers).text

    # Hack to rebase the URLs
    html = re.sub('src="/(?!/)', 'src="//wiki.dolphin-emu.org/', html)
    html = re.sub('href="/(?!/)', 'href="//wiki.dolphin-emu.org/', html)
    html = re.sub(r'srcset="/([^/].*) 1\.5x, /(?!/)', r'srcset="//wiki.dolphin-emu.org/\1 1.5x, //wiki.dolphin-emu.org/', html)

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
        po.append(polib.POEntry(msgid=cat.title, msgstr='', msgctxt='Category title'))
        for q in cat.sorted_questions():
            po.append(polib.POEntry(msgid=q.title, msgstr='', msgctxt='Question title'))
            po.append(polib.POEntry(msgid=q.short_title, msgstr='',
                                    msgctxt='Question short title (displayed in the left column)'))
            po.append(polib.POEntry(msgid=q.text, msgstr='', msgctxt='Answer'))
    return HttpResponse(po)
