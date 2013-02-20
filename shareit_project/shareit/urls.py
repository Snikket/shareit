from django.conf.urls import patterns, url

from shareit import views

urlpatterns = patterns('',
	url(r'^$',views.home, name='home'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'restricted', views.restricted, name='restricted'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^category/$', views.category, name='category'),
)
