from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'search.views.home', name='home'),
    # url(r'^search/', include('search.foo.urls')),
    #url(r'^tools/', include('search.foo.urls')), #odd

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # search urls
    url(r'^$', 'search.views.index'),
)
