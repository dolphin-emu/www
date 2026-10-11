# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.db import models
from dolweb.downloads.models import DownloadableVersion

class UpdateTrack(models.Model):
    name = models.CharField(max_length=64, db_index=True)
    version = models.ForeignKey(
        DownloadableVersion,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='update_tracks')
    version_name = models.CharField(max_length=64, null=True)
    changelog_text = models.TextField()

    def __str__(self):
        return 'Track %s, version %s' % (self.name, self.version)

    class Meta:
        unique_together = ('name', 'version')
        indexes = [
            models.Index(fields=['name', 'version'], name='update_track_name_version_idx'),
        ]
