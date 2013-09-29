from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _

from zinnia.settings import UPLOAD_TO
from zinnia.managers import PUBLISHED
# from zinnia.models.entry import Entry


class BlogSerie(models.Model):
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
        """Returns the 1-indexed nth article in serie."""
        if nth < 1:
            return None

        qs = self.entries.all()
        if not allow_hidden:
            qs = qs.filter(status=PUBLISHED)

        try:
            return qs.order_by('creation_date')[nth - 1]
        except IndexError:
            return None

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<BlogSerie "%s" (%d entries)>' % (self.name, self.entries.count())


class ForumThreadForEntry(models.Model):
    entry = models.OneToOneField('zinnia.Entry', related_name='forum_thread', null=True, blank=True)
    thread_id = models.IntegerField()

    def get_absolute_url(self):
        return settings.FORUM_URL_FOR_THREAD.format(id=self.thread_id)

    def __unicode__(self):
        return "%s -> %s" % (self.entry, self.get_absolute_url())

    def __repr__(self):
        return "<ForumThreadForEntry %s -> thread %d>" % (
            self.entry, self.thread_id
        )
