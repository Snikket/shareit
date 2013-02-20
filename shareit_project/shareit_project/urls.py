from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^shareit/', include('shareit.urls')),
	# Examples:
	# url(r'^$', 'shareit_project.views.home', name='home'),
	# url(r'^shareit_project/', include('shareit_project.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^shareit/', include('shareit.urls')),
        url(r'^admin/', include(admin.site.urls)),
)
