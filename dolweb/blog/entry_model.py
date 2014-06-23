from django.db import models
from zinnia.models.entry import EntryAbstractClass
from django.utils.translation import ugettext as _

from models import BlogSeries

# Why this file?
# "Do not put your abstract model in a file named models.py, it will not work
#  for a non obvious reason."
# http://django-blog-zinnia.readthedocs.org/en/v0.12.3/how-to/extending_entry_model.html#writing-model-extension


class BlogEntry(EntryAbstractClass):
    """
    Represents a blog entry. Adds an optional `series` field to the default
    Zinnia model.
    """
    within_series = models.ForeignKey(BlogSeries, null=True, blank=True, related_name='entries')

    @property
    def real_image(self):
        """Priorities the entry image, then the series image, if any."""
        if self.image:
            return self.image

        if self.within_series is not None:
            # May be None!
            return self.within_series.image

    @property
    def series_index(self):
        if self.within_series is None:
            return 1

        return (self.within_series.entries
            .filter(creation_date__lt=self.creation_date)
            .exclude(pk=self.pk)
            .count()) + 1

    def relative_entry_in_series(self, offset):
        if self.within_series is None:
            return None

        return self.within_series.nth_entry(self.series_index + offset)

    @property
    def next_entry_in_series(self):
        return self.relative_entry_in_series(1)

    @property
    def previous_entry_in_series(self):
        return self.relative_entry_in_series(-1)

    class Meta(EntryAbstractClass.Meta):
        abstract = True
