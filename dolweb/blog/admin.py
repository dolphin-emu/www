from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from zinnia.models.entry import Entry
from zinnia.admin.entry import EntryAdmin
from dolweb.blog.models import BlogSeries, ForumThreadForEntry

class BlogSeriesAdmin(admin.ModelAdmin):
    pass

class ForumThreadForEntryAdmin(admin.ModelAdmin):
    pass

class BlogEntryAdmin(EntryAdmin):
  # In our case we put the gallery field
  # into the 'Content' fieldset
  fieldsets = ((_('Content'), {'fields': (
    'title', 'content', 'image', 'status', 'within_series')}),) + \
    EntryAdmin.fieldsets[1:]


admin.site.register(Entry, BlogEntryAdmin)
admin.site.register(BlogSeries, BlogSeriesAdmin)
admin.site.register(ForumThreadForEntry, ForumThreadForEntryAdmin)
