from django.db import models
from dolweb.downloads.models import DevVersion

class UpdateTrack(models.Model):
    name = models.CharField(max_length=64, db_index=True)
    version = models.ForeignKey(
        DevVersion, db_index=True, related_name='update_tracks')
    version_name = models.CharField(max_length=64, null=True)
    changelog_text = models.TextField()

    def __unicode__(self):
        return 'Track %s, version %s' % (self.name, self.version)

    class Meta:
        unique_together = ('name', 'version')
        index_together = ('name', 'version')
