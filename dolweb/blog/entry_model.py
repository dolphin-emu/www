from django.db import models
from zinnia.models_bases.entry import AbstractEntry
from django.utils.translation import ugettext as _

from dolweb.blog.models import BlogSerie

# Why this file?
# "Do not put your abstract model in a file named models.py, it will not work
#  for a non obvious reason."
# http://django-blog-zinnia.readthedocs.org/en/v0.12.3/how-to/extending_entry_model.html#writing-model-extension


class BlogEntry(AbstractEntry):
    """
    Represents a blog entry. Adds an optional `serie` field to the default
    Zinnia model.
    """
    within_serie = models.ForeignKey(BlogSerie, null=True, blank=True, related_name='entries')

    @property
    def real_image(self):
        """Priorities the entry image, then the serie image, if any."""
        if self.image:
            return self.image

        if self.within_serie is not None:
            # May be None!
            return self.within_serie.image

    @property
    def serie_index(self):
        if self.within_serie is None:
            return 1

        return (self.within_serie.entries
            .filter(creation_date__lt=self.creation_date)
            .exclude(pk=self.pk)
            .count()) + 1

    def relative_entry_in_serie(self, offset):
        if self.within_serie is None:
            return None

        return self.within_serie.nth_entry(self.serie_index + offset)

    @property
    def next_entry_in_serie(self):
        return self.relative_entry_in_serie(1)

    @property
    def previous_entry_in_serie(self):
        return self.relative_entry_in_serie(-1)

    class Meta(AbstractEntry.Meta):
        abstract = True
