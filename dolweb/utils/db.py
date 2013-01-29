class WikiRouter(object):
    """
    Routes access to wiki/compat models to the wiki database, and everything
    else to the default database.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'compat':
            return 'wiki'
        return 'default'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, o1, o2, **hints):
        return None

    def allow_syncdb(self, db, model):
        return (db != 'wiki')
