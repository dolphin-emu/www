# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView
from dolweb.homepage.views import home
from dolweb.management.views import run_command

# Monkey patching ftw...
import dolweb.utils.monkey

admin.autodiscover()

urlpatterns = [
    # Homepage
    url(r'^$', home, name='home'),

    # Media (image gallery, link to videos)
    url(r'^media/', include('dolweb.media.urls')),

    # Documentation (FAQ and guides)
    url(r'^docs/', include('dolweb.docs.urls')),

    # Downloads
    url(r'^download/', include('dolweb.downloads.urls')),

    # Blog
    url(r'^blog/', include('dolweb.blog.urls')),

    # Compatibility list
    url(r'^compat/', include('dolweb.compat.urls')),

    # Django administration
    url(r'^admin/', admin.site.urls),

    # Management interface
    url(r'^mgmt/(?P<cmd>.+)$', run_command, name='mgmt_run_command'),

    # Auto-update checking.
    url(r'^update/', include('dolweb.update.urls')),

    # ads.txt
    url(r"^ads.txt$", RedirectView.as_view(url=staticfiles_storage.url("ads.txt"))),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
