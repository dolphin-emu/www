# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.contrib import admin
from dolweb.downloads.models import Artifact, BranchInfo, DownloadableVersion, ReleaseVersion, DevVersion

class DownloadableVersionAdmin(admin.ModelAdmin):
    # The shared version model supplies the update-track autocomplete only.
    search_fields = ('^shortrev',)
    ordering = ('-date', '-pk')

    def get_model_perms(self, request):
        return {}

    def has_view_permission(self, request, obj=None):
        return (super().has_view_permission(request, obj)
                or request.user.has_perm('update.add_updatetrack')
                or request.user.has_perm('update.change_updatetrack'))

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(DownloadableVersion, DownloadableVersionAdmin)

class BranchInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'visible')
    ordering = ('-visible', 'name')
admin.site.register(BranchInfo, BranchInfoAdmin)

class ArtifactAdmin(admin.StackedInline):
    model = Artifact

class ReleaseVersionAdmin(admin.ModelAdmin):
    list_display = ('shortrev', 'date')
    ordering = ('-date',)
    inlines = [ArtifactAdmin]
admin.site.register(ReleaseVersion, ReleaseVersionAdmin)

class DevVersionAdmin(admin.ModelAdmin):
    list_display = ('revbranch', 'hash', 'date', 'author')
    ordering = ('-date',)
    inlines = [ArtifactAdmin]
admin.site.register(DevVersion, DevVersionAdmin)
