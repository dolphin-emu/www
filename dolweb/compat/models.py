# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.db.models import QuerySet

import urllib.parse

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

    def __str__(self):
        return 'Blob %d: %s' % (self.id, self.data[:100])

    class Meta:
        db_table = 'text'
        verbose_name = 'MediaWiki Text Blob'
        verbose_name_plural = 'MediaWiki Text Blobs'

class Content(models.Model):
    id = models.BigIntegerField(db_column='content_id', primary_key=True)
    address = models.CharField(db_column='content_address', max_length=255)

    @property
    def text_id(self):
        address = self.address
        if isinstance(address, bytes):
            address = address.decode('ascii')
        if not address.startswith('tt:'):
            raise ValueError('Unsupported MediaWiki content address: %s' % address)
        return int(address[3:])

    @property
    def text(self):
        if not hasattr(self, '_text_cache'):
            self._text_cache = Text.objects.get(id=self.text_id)
        return self._text_cache

    class Meta:
        db_table = 'content'
        verbose_name = 'MediaWiki Content'
        verbose_name_plural = 'MediaWiki Contents'

class SlotRole(models.Model):
    id = models.IntegerField(db_column='role_id', primary_key=True)
    name = models.CharField(db_column='role_name', max_length=64)

    class Meta:
        db_table = 'slot_roles'
        verbose_name = 'MediaWiki Slot Role'
        verbose_name_plural = 'MediaWiki Slot Roles'

class Slot(models.Model):
    revision = models.ForeignKey('Revision', on_delete=models.PROTECT, db_column='slot_revision_id',
                                 primary_key=True, related_name='+')
    role = models.ForeignKey('SlotRole', on_delete=models.PROTECT, db_column='slot_role_id',
                             related_name='+')
    content = models.ForeignKey('Content', on_delete=models.PROTECT, db_column='slot_content_id',
                                related_name='+')
    origin = models.ForeignKey('Revision', on_delete=models.PROTECT, db_column='slot_origin',
                               related_name='+')

    @property
    def text(self):
        return self.content.text

    class Meta:
        db_table = 'slots'
        verbose_name = 'MediaWiki Slot'
        verbose_name_plural = 'MediaWiki Slots'

class Revision(models.Model):
    id = models.IntegerField(db_column='rev_id', primary_key=True)
    page = models.ForeignKey('Page', on_delete=models.PROTECT, db_column='rev_page', related_name='+')
    timestamp = models.CharField(db_column='rev_timestamp', max_length=14)

    @property
    def text(self):
        if not hasattr(self, '_text_cache'):
            self._text_cache = Slot.objects.get(revision=self, role__name='main').text
        return self._text_cache

    def __str__(self):
        return '%s for %s' % (self.timestamp, self.page)

    class Meta:
        db_table = 'revision'
        verbose_name = 'MediaWiki Revision'
        verbose_name_plural = 'MediaWiki Revisions'

class PageQuerySet(QuerySet):
    def with_latest_text_in(self, values):
        if not values:
            return self.none()

        placeholders = ', '.join(['%s'] * len(values))
        return self.extra(where=[("""
            EXISTS (
                SELECT 1
                FROM "slots" slot
                INNER JOIN "slot_roles" role ON role."role_id" = slot."slot_role_id"
                INNER JOIN "content" content ON content."content_id" = slot."slot_content_id"
                INNER JOIN "text" text ON text."old_id" = CAST(SUBSTRING(content."content_address" FROM 4) AS INTEGER)
                WHERE slot."slot_revision_id" = "page"."page_latest"
                    AND role."role_name" = %s
                    AND content."content_address" LIKE %s
                    AND text."old_text" IN ({placeholders})
            )
        """).format(placeholders=placeholders)], params=['main', 'tt:%'] + list(values))

class Page(models.Model):
    id = models.IntegerField(db_column='page_id', primary_key=True)
    namespace = models.IntegerField(db_column='page_namespace')
    title_url = models.CharField(db_column='page_title', max_length=255)
    len = models.IntegerField(db_column='page_len')
    latest = models.ForeignKey('Revision', on_delete=models.PROTECT, db_column='page_latest', related_name='+')
    is_redirect = models.BooleanField(db_column='page_is_redirect', default=False)

    objects = PageQuerySet.as_manager()

    @property
    def wiki_url(self):
        u = self.title_url
        if u.startswith('Ratings/'):
            u = u[len('Ratings/'):]
        return settings.WIKI_URL + 'index.php?title=%s' % urllib.parse.quote(u)

    @property
    def title(self):
        s = self.title_url.replace('_', ' ')
        if s.startswith('Ratings/'):
            s = s[len('Ratings/'):]
        return s

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'page'
        ordering = ['namespace', 'title_url']
        verbose_name = 'MediaWiki Page'
        verbose_name_plural = 'MediaWiki Pages'

class Category(models.Model):
    id = models.IntegerField(db_column='cat_id', primary_key=True)
    title = models.CharField(db_column='cat_title', max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'category'
        ordering = ['title']
        verbose_name = 'MediaWiki Category'
        verbose_name_plural = 'MediaWiki Categories'

class LinkTarget(models.Model):
    id = models.BigIntegerField(db_column='lt_id', primary_key=True)
    namespace = models.IntegerField(db_column='lt_namespace')
    title_url = models.CharField(db_column='lt_title', max_length=255)

    @property
    def title(self):
        if isinstance(self.title_url, bytes):
            return self.title_url.decode('utf-8')
        return self.title_url

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'linktarget'
        ordering = ['namespace', 'title_url']
        verbose_name = 'MediaWiki Link Target'
        verbose_name_plural = 'MediaWiki Link Targets'

class CategoryLink(models.Model):
    id = models.IntegerField(primary_key=True, db_column='cl_sortkey') ## UGLY, not PK in DB
    page = models.ForeignKey('Page', on_delete=models.PROTECT, db_column='cl_from', related_name='+')
    target = models.ForeignKey('LinkTarget', on_delete=models.PROTECT, db_column='cl_target_id',
                               related_name='+')

    @property
    def cat(self):
        return self.target.title

    def __str__(self):
        return 'Link from %s to %s' % (self.page, self.cat)

    class Meta:
        db_table = 'categorylinks'
        ordering = ['target__title_url', 'page']
        verbose_name = 'MediaWiki Category Link'
        verbose_name_plural = 'MediaWiki Category Links'

def populate_latest_text(pages):
    revisions = {page.latest_id: page.latest for page in pages}
    if not revisions:
        return

    slots = (Slot.objects.filter(revision_id__in=revisions.keys(), role__name='main')
                         .select_related('content'))
    slots = list(slots)
    contents = {}
    for slot in slots:
        contents[slot.content.text_id] = slot.content

    texts = Text.objects.in_bulk(contents.keys())
    for text_id, content in contents.items():
        text = texts.get(text_id)
        if text is None:
            continue
        content._text_cache = text
        for slot in slots:
            if slot.content_id == content.id:
                revisions[slot.revision_id]._text_cache = text

def get_rated_games():
    count = cache.get('rating_count')
    if count is None:
        count = Page.objects.with_latest_text_in(('1', '2', '3', '4', '5')).filter(
            namespace=Namespace.TEMPLATE, title_url__startswith='Ratings/').count()
        cache.set('rating_count', count, 300)
    return count

def get_rating_count(n):
    if n < 1 or n > 5:
        return 0

    count = cache.get('rating_count_%d' % n)
    if count is None:
        count = Page.objects.with_latest_text_in((str(n),)).filter(
            namespace=Namespace.TEMPLATE, title_url__startswith='Ratings/').count()
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
