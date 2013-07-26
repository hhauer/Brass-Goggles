from django.conf.urls import patterns, url

from private_api import views

urlpatterns = patterns('',
    url(r'^gametask/(?P<game_name>[-\w]+)/(?P<task_id>\d+)/(?P<status>(S|I|U|F))$', views.gametask_api),
)