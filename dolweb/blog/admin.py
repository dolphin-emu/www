# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.conf import settings
from django.contrib import admin
from django.forms import Widget
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from zinnia.models.entry import Entry
from zinnia.admin.entry import EntryAdmin
from zinnia.admin.forms import EntryAdminForm
from dolweb.blog.models import BlogSeries, ForumThreadForEntry

class BlogSeriesAdmin(admin.ModelAdmin):
    pass

class ForumThreadForEntryAdmin(admin.ModelAdmin):
    pass

class EtherpadWidget(Widget):
    def __init__(self, pad_id):
        super(EtherpadWidget, self).__init__()
        self.pad_id = pad_id

    def render(self, *args, **kwargs):
        return render_to_string('etherpad-widget.html',
                { 'BLOG_ETHERPAD_URL': settings.BLOG_ETHERPAD_URL,
                  'pad_id': self.pad_id })

class BlogEntryAdminForm(EntryAdminForm):
    def __init__(self, *args, **kwargs):
        super(BlogEntryAdminForm, self).__init__(*args, **kwargs)
        self._instance = kwargs.get('instance')
        if self._instance and self._instance.use_collaborative_editing:
            self.fields['content'].widget = EtherpadWidget(self._instance.etherpad_id)

    def clean(self, *args, **kwargs):
        cleaned_data = super(BlogEntryAdminForm, self).clean(*args, **kwargs)
        if self._instance and self._instance.use_collaborative_editing:
            del cleaned_data['content']
        return cleaned_data

class BlogEntryAdmin(EntryAdmin):
    form = BlogEntryAdminForm

    fieldsets = ((_('Content'), {
        'fields': (('title', 'status'), 'lead', 'content', 'within_series')
    }),) + EntryAdmin.fieldsets[1:]


admin.site.register(Entry, BlogEntryAdmin)
admin.site.register(BlogSeries, BlogSeriesAdmin)
admin.site.register(ForumThreadForEntry, ForumThreadForEntryAdmin)
