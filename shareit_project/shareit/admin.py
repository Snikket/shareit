from django.contrib import admin
from django.db import models
from shareit.models import Category, Post, Rating, UserProfile, Followers

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Rating)
admin.site.register(UserProfile)
class FollowInterface(admin.ModelAdmin):
	fieldsets = [
		('User',		{'fields':['fuser']}),
		('Follows', {'fields':['follows']} )
	]

admin.site.register(Followers, FollowInterface )
