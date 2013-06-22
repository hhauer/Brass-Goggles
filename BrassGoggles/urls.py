from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'Laboratory.views.index'),
    url(r'^laboratory/', include('Laboratory.urls')),
    
    url(r'^accounts/', include('registration.backends.default.urls')),
    # Examples:
    # url(r'^$', 'BrassGoggles.views.home', name='home'),
    # url(r'^BrassGoggles/', include('BrassGoggles.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
