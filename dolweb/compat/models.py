from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from django.db import models

import urllib

class Namespace(object):
    MAIN = 0
    TALK = 1
    USER = 2
    USER_TALK = 3
    PROJECT = 4
    PROJECT_TALK = 5
    FILE = 6
    FILE_TALK = 7
    MEDIAWIKI = 8
    MEDIAWIKI_TALK = 9
    TEMPLATE = 10
    TEMPLATE_TALK = 11
    HELP = 12
    HELP_TALK = 13
    CATEGORY = 14
    CATEGORY_TALK = 15

class Text(models.Model):
    id = models.IntegerField(db_column='old_id', primary_key=True)
    data_raw = models.TextField(db_column='old_text')

    @property
    def data(self):
        return self.data_raw

    def __unicode__(self):
        return u'Blob %d: %s' % (self.id, self.data[:100])

    class Meta:
        db_table = 'pagecontent'
        verbose_name = u'MediaWiki Text Blob'
        verbose_name_plural = u'MediaWiki Text Blobs'

class Revision(models.Model):
    id = models.IntegerField(db_column='rev_id', primary_key=True)
    page = models.ForeignKey('Page', db_column='rev_page', related_name='+')
    text = models.ForeignKey('Text', db_column='rev_text_id', related_name='+')
    timestamp = models.CharField(db_column='rev_timestamp', max_length=14)

    def __unicode__(self):
        return u'%s for %s' % (self.timestamp_raw, self.page)

    class Meta:
        db_table = 'revision'
        verbose_name = u'MediaWiki Revision'
        verbose_name_plural = u'MediaWiki Revisions'

class Page(models.Model):
    id = models.IntegerField(db_column='page_id', primary_key=True)
    namespace = models.IntegerField(db_column='page_namespace')
    title_url = models.CharField(db_column='page_title', max_length=255)
    len = models.IntegerField(db_column='page_len')
    latest = models.ForeignKey('Revision', db_column='page_latest', related_name='+')
    is_redirect = models.BooleanField(db_column='page_is_redirect', default=False)

    @property
    def wiki_url(self):
        u = self.title_url.encode('utf-8')
        if u.startswith('Ratings/'):
            u = u[len('Ratings/'):]
        return settings.WIKI_URL + 'index.php?title=%s' % urllib.quote(u)

    @property
    def title(self):
        s = self.title_url.replace('_', ' ')
        if s.startswith('Ratings/'):
            s = s[len('Ratings/'):]
        return s

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'page'
        ordering = ['namespace', 'title_url']
        verbose_name = u'MediaWiki Page'
        verbose_name_plural = u'MediaWiki Pages'

class Category(models.Model):
    id = models.IntegerField(db_column='cat_id', primary_key=True)
    title = models.CharField(db_column='cat_title', max_length=255)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'category'
        ordering = ['title']
        verbose_name = u'MediaWiki Category'
        verbose_name_plural = u'MediaWiki Categories'

class CategoryLink(models.Model):
    id = models.IntegerField(primary_key=True, db_column='cl_sortkey') ## UGLY, not PK in DB
    page = models.ForeignKey('Page', db_column='cl_from', related_name='+')
    cat = models.CharField(db_column='cl_to', max_length=255)

    def __unicode__(self):
        return u'Link from %s to %s' % (self.page, self.cat)

    class Meta:
        db_table = 'categorylinks'
        ordering = ['cat', 'page']
        verbose_name = u'MediaWiki Category Link'
        verbose_name_plural = u'MediaWiki Category Links'

def get_rated_games():
    count = cache.get('rating_count')
    if count is None:
        count = Page.objects.filter(namespace=Namespace.TEMPLATE, title_url__startswith='Ratings/',
                                    latest__text__data_raw__in=('1', '2', '3', '4', '5')).count()
        cache.set('rating_count', count, 300)
    return count

def get_rating_count(n):
    if n < 1 or n > 5:
        return 0

    count = cache.get('rating_count_%d' % n)
    if count is None:
        count = Page.objects.filter(namespace=Namespace.TEMPLATE, title_url__startswith='Ratings/',
                                    latest__text__data_raw=str(n)).count()
        cache.set('rating_count_%d' % n, count, 300)

    return count

def get_category_id(name):
    id = cache.get('category_name_%s' % name)
    if id is None:
        try:
            id = Category.objects.get(title=name)
        except Category.DoesNotExist:
            return 0
        cache.set('category_name_%s' % name, id)

    return id
