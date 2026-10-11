# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.conf import settings

class WikiRouter(object):
    """
    Routes access to wiki/compat models to the wiki database, and everything
    else to the default database.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'compat':
            return settings.WIKI_DB_NAME
        return 'default'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, o1, o2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'wiki':
            return not settings.WIKI_DB_READ_ONLY
        return True
