from annoying.decorators import render_to
from django.shortcuts import get_object_or_404
from dolweb.docs.models import FAQCategory, FAQ, Guide

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
