# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.contrib import admin
from dolweb.downloads.models import Artifact, BranchInfo, ReleaseVersion, DevVersion

class BranchInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'visible')
    ordering = ('-visible', 'name')
admin.site.register(BranchInfo, BranchInfoAdmin)

class ArtifactAdmin(admin.StackedInline):
    model = Artifact

class ReleaseVersionAdmin(admin.ModelAdmin):
    list_display = ('version', 'date')
    ordering = ('-date',)
    inlines = [ArtifactAdmin]
admin.site.register(ReleaseVersion, ReleaseVersionAdmin)

class DevVersionAdmin(admin.ModelAdmin):
    list_display = ('revbranch', 'hash', 'date', 'author')
    ordering = ('-date',)
    inlines = [ArtifactAdmin]
admin.site.register(DevVersion, DevVersionAdmin)
