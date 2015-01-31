from django.conf.urls import patterns, url

urlpatterns = patterns('dolweb.docs.views',
    url(r'faq/$', 'faq', name='docs_faq'),
    url(r'faq/template.po$', 'faq_dyni18n_po', name='docs_faq_dyni18n_po'),
    url(r'guides/$', 'guides_index', name='docs_guides_index'),
    url(r'guides/(?P<slug>[\w-]+)/$', 'guide', name='docs_guide'),
)
