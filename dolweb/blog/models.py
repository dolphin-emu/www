# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.conf import settings
from django.db import models
from django.utils.html import linebreaks
from django.utils.translation import ugettext as _

from zinnia.markups import textile
from zinnia.markups import markdown
from zinnia.markups import restructuredtext
from zinnia.settings import UPLOAD_TO, MARKUP_LANGUAGE
from zinnia.managers import PUBLISHED
from zinnia.models_bases.entry import AbstractEntry


class BlogSeries(models.Model):
    """Represents a date-ordered sequence of blog entries."""

    name = models.CharField(max_length=255, db_index=True)
    visible = models.BooleanField(default=True)
    image = models.ImageField(
        _('image'), blank=True, upload_to=UPLOAD_TO,
        help_text=_('Used for illustration.'))

    @property
    def entries_reversed(self):
        return self.entries.order_by('creation_date')

    def nth_entry(self, nth, allow_hidden=False):
        """Returns the 1-indexed nth article in series."""
        if nth < 1:
            return None

        qs = self.entries.all()
        if not allow_hidden:
            qs = qs.filter(status=PUBLISHED)

        try:
            return qs.order_by('creation_date')[nth - 1]
        except IndexError:
            return None

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<BlogSeries "%s" (%d entries)>' % (self.name, self.entries.count())


class ForumThreadForEntry(models.Model):
    entry = models.OneToOneField('zinnia.Entry', on_delete=models.CASCADE, related_name='forum_thread')
    thread_id = models.IntegerField()

    def get_absolute_url(self):
        return settings.FORUM_URL_FOR_THREAD.format(id=self.thread_id)

    def __str__(self):
        return "%s -> %s" % (self.entry, self.get_absolute_url())

    def __repr__(self):
        return "<ForumThreadForEntry %s -> thread %d>" % (
            self.entry, self.thread_id
        )

class BlogEntry(AbstractEntry):
    """
    Represents a blog entry. Adds an optional `series` field to the default
    Zinnia model.
    """
    within_series = models.ForeignKey(BlogSeries, on_delete=models.SET_NULL, null=True, blank=True, related_name='entries')
    etherpad_id = models.CharField(max_length=256, null=True, blank=True)

    @property
    def use_collaborative_editing(self):
        return self.etherpad_id and self.draft

    @property
    def draft(self):
        return self.status != PUBLISHED

    # The default Zinnia implementation of this does stupid content sniffing,
    # assuming that if something contains </p> it is raw HTML. That's not true,
    # since Markdown can contain HTML.
    @property
    def html_content(self):
        """
        Returns the "content" field formatted in HTML.
        """
        if MARKUP_LANGUAGE == 'markdown':
            # TODO: Remove when Zinnia supports non-string Markdown exts.
            import markdown
            from zinnia.settings import MARKDOWN_EXTENSIONS
            from django.utils.encoding import force_text
            return markdown.markdown(force_text(self.content),
                                     extensions=MARKDOWN_EXTENSIONS,
                                     safe_mode=False)
        elif MARKUP_LANGUAGE == 'textile':
            return textile(self.content)
        elif MARKUP_LANGUAGE == 'restructuredtext':
            return restructuredtext(self.content)
        return linebreaks(self.content)

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

    class Meta(AbstractEntry.Meta):
        abstract = True
