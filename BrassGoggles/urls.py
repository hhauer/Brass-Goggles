from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'Laboratory.views.index'),
    url(r'^laboratory/', include('Laboratory.urls')),
    url(r'^private_api/', include('private_api.urls')),
    
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
