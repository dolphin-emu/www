from django.conf.urls import patterns, url

urlpatterns = patterns('dolweb.docs.views',
    url(r'faq/$', 'faq', name='docs-faq'),
    url(r'guides/$', 'guides_index', name='docs-guides-index'),
    url(r'guides/(?P<slug>[\w-]+)/$', 'guide', name='docs-guide'),
)
