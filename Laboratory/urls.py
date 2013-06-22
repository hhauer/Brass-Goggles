from django.conf.urls import patterns, url

from Laboratory import views

urlpatterns = patterns('',
    url(r'^periodic_table/$', views.periodic_table),
    url(r'^periodic_table/(?P<element>\w+)/$', views.element_detail),
)