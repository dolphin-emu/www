from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    # Homepage
    url(r'^$', 'dolweb.homepage.views.home', name='home'),
    url(r'^news/(?P<slug>[\w-]+)/$', 'dolweb.homepage.views.news_article',
        name='news-article'),

    # Documentation (FAQ and guides)
    url(r'^docs/', include('dolweb.docs.urls')),

    # Downloads
    url(r'^download/', include('dolweb.downloads.urls')),

    # Django administration
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
