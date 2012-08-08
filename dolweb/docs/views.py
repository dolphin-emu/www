from django.shortcuts import render_to_response
from django.template import RequestContext
from dolweb.docs.models import FAQCategory, FAQ, Guide

def faq(request):
    categories = FAQCategory.objects.order_by('display_order')
    categories = categories.prefetch_related('questions')
    
    return render_to_response('docs-faq.html', { 'categories': categories },
                              context_instance=RequestContext(request))

def guides_index(request):
    raise NotImplemented

def guide(request):
    raise NotImplemented
