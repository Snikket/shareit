from django.contrib import admin
from django.db import models
from shareit.models import Category, Post, Rating, UserProfile

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Rating)
admin.site.register(UserProfile)

