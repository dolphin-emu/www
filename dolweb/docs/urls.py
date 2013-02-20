from django.conf.urls import patterns, url

urlpatterns = patterns('dolweb.docs.views',
    url(r'faq/$', 'faq', name='docs-faq'),
    url(r'faq/template.po$', 'faq_dyni18n_po', name='docs-faq-dyni18n-po'),
    url(r'guides/$', 'guides_index', name='docs-guides-index'),
    url(r'guides/(?P<slug>[\w-]+)/$', 'guide', name='docs-guide'),
)
