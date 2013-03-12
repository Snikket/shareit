from django.conf.urls import patterns, url

from shareit import views

urlpatterns = patterns('',
	url(r'^$',views.home, name='home'),
   	url(r'^cat_filter/(?P<name>\w+)', views.filteredhome, name='filteredhome'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'followers', views.followers, name='followers'),
	url(r'following', views.following, name='following'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^category/$', views.category, name='category'),
	url(r'^followUser/(?P<username>\w+)', views.followUser, name='followUser'),
	url(r'^unfollowUser/(?P<username>\w+)', views.unfollowUser, name='unfollowUser'),
	url(r'^profiles/(?P<name>\w+)', views.user_profiles, name='profile'),
	url(r'^cat_post/(?P<category_name>\w+)', views.cat_post, name='cat_post'),
	url(r'^add_post/$', views.add_post, name='add_post'),
	url(r'^post_tu', views.tup_post, name='post_tu'),
	url(r'^post_tdown', views.tdown_post, name='post_tdown'),
	url(r'^add_comment/(?P<post_id>\w+)', views.add_comment, name='add_comment'),
	url(r'^mostPop', views.mostPop, name='MostPop'),
	url(r'^leastPop', views.leastPop, name='leastPop'),
)
