from django.contrib import admin
from django.db import models
from shareit.models import Category, Post, UserProfile, Followers, postComment, Link

admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(postComment)
class FollowInterface(admin.ModelAdmin):
	fieldsets = [
		('User',		{'fields':['fuser']}),
		('Follows', {'fields':['follows']} )
	]

class CommentInline(admin.StackedInline):
	model = postComment
	extra = 0

class LinkInLine(admin.StackedInline):
	model = Link
	extra = 0

class Postin(admin.ModelAdmin):
	inlines = [CommentInline, LinkInLine]

admin.site.register(Post, Postin)
admin.site.register(Followers, FollowInterface )
