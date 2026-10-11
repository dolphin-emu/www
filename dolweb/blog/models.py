# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.conf import settings
from django.db import models


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
