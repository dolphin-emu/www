from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from dolweb.docs.models import FAQCategory, FAQ, Guide

def faq(request):
    categories = FAQCategory.objects.order_by('display_order')
    categories = categories.prefetch_related('questions')
    
    return render_to_response('docs-faq.html', { 'categories': categories },
                              context_instance=RequestContext(request))

def guides_index(request):
    guides = Guide.objects.filter(published=True).order_by('title')
    return render_to_response('docs-guides-index.html', { 'guides': guides },
                              context_instance=RequestContext(request))

def guide(request, slug):
    guide = get_object_or_404(Guide, slug=slug)
    return render_to_response('docs-guide.html', { 'guide': guide },
                              context_instance=RequestContext(request))
