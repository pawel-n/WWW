from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^gmina/(?P<gmina_id>[0-9]+)/$', views.gmina, name='gmina'),
    url(r'^obwód/(?P<obwód_id>[0-9]+)/$', views.obwód, name='obwód')
]