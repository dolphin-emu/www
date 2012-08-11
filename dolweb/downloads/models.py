from django.db import models
from django.utils.translation import ugettext as _

class DownloadableVersion(models.Model):
    """Abstract model definining the download links for a downloadable version
    of Dolphin."""

    win32_url = models.URLField(null=True)
    win64_url = models.URLField(null=True)
    osx_url = models.URLField(null=True)

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
        return ('downloads-view-release', [self.version])

class DevVersion(DownloadableVersion):
    """Download infos for a developement/nightly release"""

    branch = models.CharField(max_length=64)
    shortrev = models.CharField(max_length=64)
    hash = models.CharField(max_length=64, db_index=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=128)
    description = models.TextField()
    description_abbrev = models.CharField(max_length=256)

    def __unicode__(self):
        if self.branch == "master":
            version = self.shortrev
        else:
            version = u"%s-%s" % (self.branch, self.shortrev)

        return _("Dolphin %s") % version

    @property
    def revbranch(self):
        return u"%s-%s" % (self.shortrev, self.branch)

    @models.permalink
    def get_absolute_url(self):
        return ('downloads-view-devrel', (), { 'hash': self.hash })
