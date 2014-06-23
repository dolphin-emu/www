from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from models import BlogSeries
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
        return reverse('dolweb.blog.views.series_index', args=[obj.pk])

    def get_title(self, obj):
        return _("Entries for the series %s") % obj.name

    def description(self, obj):
        return _("The latest entries for the series %s") % obj.name
