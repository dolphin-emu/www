from annoying.decorators import render_to
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from dolweb.docs.models import FAQCategory, FAQ, Guide

import polib

@render_to('docs-faq.html')
def faq(request):
    categories = FAQCategory.objects.order_by('display_order')
    categories = categories.prefetch_related('questions')

    return { 'categories': categories }

@render_to('docs-guides-index.html')
def guides_index(request):
    guides = Guide.objects.filter(published=True).order_by('title')
    return { 'guides': guides }

@render_to('docs-guide.html')
def guide(request, slug):
    guide = get_object_or_404(Guide, slug=slug)
    return { 'guide': guide }

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
