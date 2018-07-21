from django.conf.urls import url
from dolweb.media import views

urlpatterns = [
    url(r'^$', views.all, name='media_all'),
]
