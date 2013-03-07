from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='imgs', blank=True)
    def __unicode__(self):
        return self.user.username
    def profile_picture(self):
    	return self.picture

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password"]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['picture']

class Followers(models.Model):
	fuser = models.ForeignKey(User)
	follows = models.ForeignKey(User, related_name='followedUser')
	def __unicode__(self):
		return self.fuser.username


class Category(models.Model):
    name = models.CharField(max_length=128,
                           unique=True)
    def __unicode__(self):
        return self.name

class Post(models.Model):
    category= models.ForeignKey(Category)
    userProfile = models.ForeignKey(UserProfile)
    postcontents = models.CharField(max_length=500, unique=False)
    thumbsup = models.IntegerField()
    thumbsdown = models.IntegerField()

    def __unicode__(self):
        return self.postcontents

class postComment(models.Model):
	text = models.CharField(max_length=1000, unique=False)
	cUser=models.ForeignKey(UserProfile)
	cPost=models.ForeignKey(Post)
	def __unicode__(self):
		return self.text

class PostForm(forms.ModelForm):
    description = forms.CharField(max_length=1000,
                                  help_text='Please enter a description for this post.')
    class Meta:
        model=Post

