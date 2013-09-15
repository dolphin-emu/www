from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from zinnia.models.entry import Entry
from zinnia.admin.entry import EntryAdmin
from dolweb.blog.models import BlogSerie, ForumThreadForEntry

class BlogSerieAdmin(admin.ModelAdmin):
    pass

class ForumThreadForEntryAdmin(admin.ModelAdmin):
    pass

class BlogEntryAdmin(EntryAdmin):
  # In our case we put the gallery field
  # into the 'Content' fieldset
  fieldsets = ((_('Content'), {'fields': (
    'title', 'content', 'image', 'status', 'within_serie')}),) + \
    EntryAdmin.fieldsets[1:]


# Unregister the default EntryAdmin
admin.site.unregister(Entry)
# then register our own
admin.site.register(Entry, BlogEntryAdmin)

admin.site.register(BlogSerie, BlogSerieAdmin)
admin.site.register(ForumThreadForEntry, ForumThreadForEntryAdmin)
