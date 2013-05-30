# from django.conf.urls import urls
# from django.conf.urls import include

from django.conf.urls import patterns

from twitteraffect import index
# import twitteraffect.crawler

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                      (r'^$', index.print_welcome),
                      (r'^crawler/$', index.print_crawling),

                       # Examples:
                       # url(r'^$', 'twitteraffect.views.home', name='home'),
                       # url(r'^twitteraffect/', include('twitteraffect.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       # url(r'^admin/', include(admin.site.urls)),
                       )
