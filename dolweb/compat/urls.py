from django.conf.urls import patterns, url

urlpatterns = patterns('dolweb.compat.views',
    url(r'^$', 'list_compat'),
    url(r'^(?P<first_char>[A-Z#])/$', 'list_compat', name='compat-list'),
)
