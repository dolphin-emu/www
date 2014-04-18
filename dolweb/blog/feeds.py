from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from dolweb.blog.models import BlogSerie
from zinnia.feeds import EntryFeed


class SerieFeed(EntryFeed):
    def get_object(self, request, pk):
        serie = get_object_or_404(BlogSerie, pk=pk)
        if not serie.visible:
            raise Http404
        return serie

    def items(self, obj):
        return obj.entries.all()[:settings.ZINNIA_FEEDS_MAX_ITEMS]

    def link(self, obj):
        return reverse('dolweb.blog.views.series_index', args=[obj.pk])

    def get_title(self, obj):
        return _("Entries for the serie %s") % obj.name

    def description(self, obj):
        return _("The latest entries for the serie %s") % obj.name
