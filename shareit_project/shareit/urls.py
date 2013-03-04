from django.conf.urls import patterns, url

from shareit import views

urlpatterns = patterns('',
	url(r'^$',views.home, name='home'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'followers', views.followers, name='followers'),
	url(r'following', views.following, name='following'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^category/$', views.category, name='category'),
    url(r'^profiles/(?P<name>\w+)', views.user_profiles, name='profile'),
        url(r'^cat_post/(?P<category_name>\w+)', views.cat_post, name='cat_post'),
)
