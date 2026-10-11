# Copyright (c) 2018 Dolphin Emulator Website Contributors
# SPDX-License-Identifier: MIT

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, re_path
from django.views.generic.base import RedirectView, TemplateView
from dolweb.homepage.views import home

# Monkey patching ftw...
import dolweb.utils.monkey

admin.autodiscover()

urlpatterns = [
    # Homepage
    re_path(r'^$', home, name='home'),

    # Media (image gallery, link to videos)
    re_path(r'^media/', include('dolweb.media.urls')),

    # Documentation (FAQ and guides)
    re_path(r'^docs/', include('dolweb.docs.urls')),

    # Downloads
    re_path(r'^download/', include('dolweb.downloads.urls')),

    # Blog
    re_path(r'^blog/', include('dolweb.blog.urls')),

    # Compatibility list
    re_path(r'^compat/', include('dolweb.compat.urls')),

    # Django administration
    re_path(r'^admin/', admin.site.urls),

    # Auto-update checking.
    re_path(r'^update/', include('dolweb.update.urls')),

    # ads.txt
    re_path(r"^ads.txt$", RedirectView.as_view(url=staticfiles_storage.url("ads.txt"))),

    # robots.txt
    re_path(r"^robots.txt$", TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]
