from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

import cgi
import re

PULL_REQUEST_FIRSTLINE_RE = re.compile(
    r'^Merge pull request #(\d+) from (\S+?)/(\S+?)$', re.U)

class BranchInfo(models.Model):
    """Used to add metadata to Dolphin Git branches (mostly visible or not)"""

    name = models.CharField(max_length=64, db_index=True)
    visible = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class DownloadableVersion(models.Model):
    """Abstract model definining the download links for a downloadable version
    of Dolphin."""

    win32_url = models.URLField(null=True)
    win64_url = models.URLField(null=True)
    osx_url = models.URLField(null=True)
    ubu_url = models.URLField(null=True)

    class Meta:
        abstract = True

class ReleaseVersion(DownloadableVersion):
    """Download infos for a release version (2.0, 3.0, ...)"""

    version = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return _("Dolphin %s") % self.version

    @models.permalink
    def get_absolute_url(self):
        return ('downloads_view_release', [self.version])

class DevVersion(DownloadableVersion):
    """Download infos for a developement/nightly release"""

    branch = models.CharField(max_length=64, db_index=True)
    shortrev = models.CharField(max_length=64)
    hash = models.CharField(max_length=64, unique=True, db_index=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=128)
    description = models.TextField()

    def __unicode__(self):
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
        return ('downloads_view_devrel', (), { 'hash': self.hash })

    @property
    def description_abbrev(self):
        """Returns HTML code that represents a short description of the changes
        in this commit."""
        lines = self.description.split(u'\n')
        match = PULL_REQUEST_FIRSTLINE_RE.match(lines[0])
        if match:
            pull_id, author, branch = match.groups()
            following_lines = [l for l in lines[1:] if l.strip() != u'']
            if not following_lines:
                short_descr = _(u'Change with no description')
            else:
                short_descr = following_lines[0]
            additional_html_fmt = _(u'(<a href="%(pr_url)s">PR #%(pr_id)s</a> from <a href="%(author_url)s">%(author)s</a>)')
            additional_html = additional_html_fmt % {
                'pr_url': settings.GIT_PR_URL % pull_id,
                'pr_id': pull_id,
                'author_url': settings.GIT_AUTHOR_URL % cgi.escape(author),
                'author': cgi.escape(author),
            }
        else:
            short_descr = lines[0]
            additional_html = u''

        if len(short_descr) >= 200:
            short_descr = short_descr[:200] + u"..."
        short_descr = cgi.escape(short_descr)
        if additional_html:
            short_descr = short_descr + u' ' + additional_html
        return mark_safe(short_descr)
