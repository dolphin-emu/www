from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext as _
from dolweb.blog.models import BlogSeries
from zinnia.feeds import EntryFeed


class SeriesFeed(EntryFeed):
    def get_object(self, request, pk):
        series = get_object_or_404(BlogSeries, pk=pk)
        if not series.visible:
            raise Http404
        return series

    def items(self, obj):
        return obj.entries.all()[:settings.ZINNIA_FEEDS_MAX_ITEMS]

    def link(self, obj):
        return reverse('dolweb_blog_series', args=[obj.pk])

    def get_title(self, obj):
        return _("Entries for the series %s") % obj.name

    def description(self, obj):
        return _("The latest entries for the series %s") % obj.name
