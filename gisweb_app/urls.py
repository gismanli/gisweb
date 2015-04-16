from django.conf.urls import patterns, url
from gisweb_app import views

urlpatterns = patterns('',
    url(r'resource/(?P<uploaded>\S+)/$', views.data_resource, name='resource'),
    url(r'^$', views.data_resource, name='resource'),
    url(r'resource$', views.data_resource, name='resource'),
    url(r'information$', views.data_information, name = 'information'),
    url(r'visualiser$', views.data_visualiser, name = 'visualiser'),
    url(r'tools$', views.tools, name = 'tools'),
)
