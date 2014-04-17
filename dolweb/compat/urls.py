from django.conf.urls import patterns, url

urlpatterns = patterns('dolweb.compat.views',
    url(r'^$', 'list_compat', name='compat-index'),
    url(r'^(?:(?P<first_char>[A-Z#])/)?(?:filter/(?P<filter_by>[12345])/)?$', 'list_compat', name='compat-list'),
)
