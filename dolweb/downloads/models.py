from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from dolweb.utils import models_utils

import cgi
import re

PULL_REQUEST_FIRSTLINE_RE = re.compile(
    r'^Merge pull request #(\d+) from (\S+?)/(\S+?)$', re.U)

class BranchInfo(models.Model):
    """Used to add metadata to Dolphin Git branches (mostly visible or not)"""

    name = models.CharField(max_length=64, db_index=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class DownloadableVersion(models.Model):
    """Base model definining the download links for a downloadable version
    of Dolphin."""

    date = models.DateTimeField(auto_now_add=True)

class ReleaseVersion(DownloadableVersion):
    """Download infos for a release version (2.0, 3.0, ...)"""

    objects = models_utils.DefaultSelectOrPrefetchManager(prefetch_related=['artifacts'])

    version = models.CharField(max_length=64)

    def __str__(self):
        return _("Dolphin %s") % self.version

    @models.permalink
    def get_absolute_url(self):
        return ('downloads_view_release', [self.version])

class DevVersion(DownloadableVersion):
    """Download infos for a developement/nightly release"""

    objects = models_utils.DefaultSelectOrPrefetchManager(prefetch_related=['artifacts'])

    branch = models.CharField(max_length=64, db_index=True)
    shortrev = models.CharField(max_length=64)
    hash = models.CharField(max_length=64, unique=True, db_index=True)
    author = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        return _("Dolphin %s") % self.revbranch

    @property
    def revbranch(self):
        if self.branch == "master":
            version = self.shortrev
        else:
            version = u"%s-%s" % (self.branch, self.shortrev)
        return version

    @models.permalink
    def get_absolute_url(self):
        return ('downloads_view_devrel_by_name', (), {'branch': self.branch, 'name': self.shortrev})

    @property
    def description_data(self):
        """Returns data that describes the changes in this commit."""
        lines = [line.strip() for line in self.description.split(u'\n')]
        match = PULL_REQUEST_FIRSTLINE_RE.match(lines[0])
        if match:
            pull_id, author, branch = match.groups()
            following_lines = [l for l in lines[1:] if l.strip() != u'']
            if not following_lines:
                short_descr = u'Change with no description'
            else:
                short_descr = following_lines[0]
            additional_data = {
                'short_descr': short_descr,
                'pr_url': settings.GIT_PR_URL % pull_id,
                'pr_id': pull_id,
                'author_url': settings.GIT_AUTHOR_URL % author,
                'author': author,
            }
        else:
            additional_data = {
                'short_descr': lines[0],
                'author': self.author,
                'author_url': settings.GIT_AUTHOR_URL % self.author,
            }
        if len(additional_data['short_descr']) >= 200:
            additional_data['short_descr'] = additional_data['short_descr'][:200] + u"..."
        return additional_data

    @property
    def description_abbrev(self):
        """Returns HTML code that represents a short description of the changes
        in this commit."""
        data = self.description_data
        if 'pr_id' in data:
            additional_html_fmt = _(u'(<a href="%(pr_url)s">PR #%(pr_id)s</a> from <a href="%(author_url)s">%(author)s</a>)')
            additional_html = additional_html_fmt % {
                'pr_url': data['pr_url'],
                'pr_id': data['pr_id'],
                'author_url': cgi.escape(data['author_url']),
                'author': cgi.escape(data['author']),
            }
        else:
            additional_html = u''

        short_descr = cgi.escape(data['short_descr'])
        if additional_html:
            short_descr = short_descr + u' ' + additional_html
        return mark_safe(short_descr)

class Artifact(models.Model):
    """Represents a downloadable object attached to a version."""

    # Shown to users. TODO: dyni18n.
    version = models.ForeignKey(DownloadableVersion, on_delete=models.CASCADE, db_index=True, related_name='artifacts')
    target_system = models.CharField(max_length=64, db_index=True)
    url = models.URLField(null=True)

    # Should match possible values from utils/context_processors.py.
    # TODO: define a known set of constants.
    user_os_matcher = models.CharField(max_length=64)

    class Meta:
        unique_together = ('version', 'target_system')
        index_together = ('version', 'target_system')
