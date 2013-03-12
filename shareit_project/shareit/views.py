from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from shareit.models import UserProfile
from shareit.models import UserForm, UserProfileForm
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from shareit.models import Category, Post, Followers, postComment, Link
from shareit_project.settings import MEDIA_ROOT
import urllib
import BeautifulSoup

import re




def home(request):
	template = loader.get_template('shareit/home.html')
	cat_list = Category.objects.all()
	posts_list=Post.objects.all().order_by('-id')
	comments_list=postComment.objects.all().order_by('-id')
	links=Link.objects.all()
	for cat in cat_list:
                cat_name = cat.name
	context = RequestContext(request, { 'links':links,'posts_list':posts_list,'cat_list': cat_list,'comments_list':comments_list, 'default_filter': '-- No Filter --'})
	return HttpResponse(template.render(context))

def followUser(request, username):
	userToFollow=User.objects.get(username=username)
	newFollower = Followers(fuser=request.user, follows=userToFollow)
	newFollower.save()
	return HttpResponseRedirect('/shareit/profiles/'+username)

def unfollowUser(request, username):
	userToUnfollow=User.objects.get(username=username)
	u = Followers.objects.get(fuser=request.user, follows=userToUnfollow).delete()
	return HttpResponseRedirect('/shareit/profiles/'+username)
	
def filteredhome(request, name):
	template = loader.get_template('shareit/home.html')
	cat_list = Category.objects.all()
	category = Category.objects.filter(name=name)
	posts_list=Post.objects.filter(category=category).order_by('-id')
	comments_list=postComment.objects.all().order_by('-id')
	for cat in cat_list:
                cat_name = cat.name
	context = RequestContext(request, { 'posts_list':posts_list,'cat_list': cat_list,'comments_list':comments_list, 'default_filter':category[0].name})
	return HttpResponse(template.render(context))

def category(request):
	template = loader.get_template('shareit/category.html')
	cat_list = Category.objects.all()
	for cat in cat_list:
                cat_name = cat.name
	context = RequestContext(request,{ 'cat_list': cat_list})
	return HttpResponse(template.render(context))

def register(request):
	context = RequestContext(request)
	registered = False
	if request.method == 'POST':
		uform = UserForm(data = request.POST)
		pform = UserProfileForm(data = request.POST)
		if uform.is_valid() and pform.is_valid():
			user = uform.save()
			#encrypts the password
			pw = user.password
			user.set_password(pw)
			user.save()
			profile = pform.save(commit = False)
			profile.user = user
			profile.save()
			#profile picture upload
			#save_file(request.FILES['picture'])
			registered = True
		else:
			print uform.errors, pform.errors
	else:
		uform = UserForm()
		pform = UserProfileForm()
	return render_to_response('shareit/register.html', {'uform':uform, 'pform':pform, 'registered':registered}, context)

# save the picture, but it doesn't work - it crashes.
#def save_file(file, path=''):
#	filename = file._get_name()
#       fd = open('%s/%s' % (MEDIA_ROOT, str(path) + str(filename)), 'wb' )
#       for chunk in file.chunks():
#               fd.write(chunk)
#       fd.close()

def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']
          user = authenticate(username=username, password=password)
          if user is not None:
              if user.is_active:
                  login(request, user)
                  # Redirect to index page.
                  return HttpResponseRedirect("/shareit/")
              else:
                  return HttpResponse("Your account is disabled.")
          else:
              print  "invalid login details " + username + " " + password
              return render_to_response('shareit/login.html', {}, context)
    else:
        # the login is a GET request, so just show the user the login form.
        return render_to_response('shareit/login.html', {}, context)

@login_required
def add_post(request):
	o=User.objects.get(username=request.user.username)
	username=request.user.username
	p=UserProfile.objects.get(user=o)
	if request.method == 'POST':
		text = request.POST['post']
		cat = request.POST['catList']
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
	newPost = Post(category=Category.objects.get(name=cat), userProfile=p, postcontents=text, thumbsup=0, thumbsdown=0)
	newPost.save()
	
	for link in urls:
		soup = BeautifulSoup.BeautifulSoup(urllib.urlopen(link))
		title= soup.title.string
		newLink=Link(title=title,url=link, linkPost=newPost)
		newLink.save()
		
		# create a new post..
		# save that post
	#return home(request)
	return HttpResponseRedirect('/shareit/')

def add_comment(request, post_id):
	o=User.objects.get(username=request.user.username)
	username = request.user.username
	p=UserProfile.objects.get(user=o)
	if request.method == 'POST':
		comments = request.POST['commentBox']
		post = Post.objects.get(id=post_id)
		newComment = postComment(text=comments, cUser=p, cPost=post)
		newComment.save()
	context_dict = {}
	return HttpResponseRedirect('/shareit/')		
	








	
@login_required
def followers(request):
	template = loader.get_template('shareit/followers.html')
	o=User.objects.get(username=request.user.username)
	following_list = Followers.objects.filter(follows=o)
	context = RequestContext(request, {'following_list':following_list})
	return HttpResponse(template.render(context))

@login_required
def following(request):
	template = loader.get_template('shareit/following.html')
	o=User.objects.get(username=request.user.username)
	following_list = Followers.objects.filter(fuser=o)
	context = RequestContext(request, {'following_list':following_list})
	return HttpResponse(template.render(context))
	

@login_required
def user_logout(request):
	context = RequestContext(request)
	logout(request)
	return HttpResponseRedirect('/shareit/')

@login_required
def user_profiles(request, name):
		currentUser=request.user.username
		cat_list = Category.objects.all()
		posts_list=Post.objects.all().order_by('-id')
		comments_list=postComment.objects.all().order_by('-id')
		links=Link.objects.all()
		if not request.user.is_authenticated():
			HttpResponseRedirect('/login/')
		userSearched=User.objects.get(username=name)
		followingList =Followers.objects.filter(fuser=request.user).values_list('follows', flat=True)
		p=UserProfile.objects.get(user=userSearched)
		picture=p.picture
		posts=Post.objects.filter(userProfile=p)
		context = RequestContext(request,{'followingList':followingList, 'currentUser':currentUser, 'picture':picture, 'user1': userSearched, 'cat_list': cat_list, 'posts_list':posts,'comments_list':comments_list,'links':links})
		return render_to_response('shareit/profile.html', {}, context )
        
def cat_post(request, category_name):
        template = loader.get_template('shareit/cat_post.html')
        cat_name = decode_category(category_name)
        context_dict={'cat_name': cat_name}
        cat = Category.objects.filter(name=cat_name)
        if cat:
                posts = Post.objects.filter(category=cat)
                context_dict['posts_list']=posts
        context = RequestContext(request, context_dict)
        return HttpResponse(template.render(context))

def encode_category(cat_name):
        return cat_name.replace(' ', '_')
        
def decode_category(cat_name):
        return cat_name.replace('_', ' ')

@login_required
def tup_post(request):
	context = RequestContext(request)
	post_id = None
	if request.method == 'GET':
		post_id = request.GET['postid']
	else:
		post_id = request.POST['postid']

	thumbsup=0
	if post_id:
		p = Post.objects.get(id=int(post_id))
		if p:
			thumbsup = p.thumbsup + 1
			p.thumbsup = thumbsup
			p.save()
	return HttpResponse(thumbsup)

@login_required
def tdown_post(request):
	context = RequestContext(request)
	post_id = None
	if request.method == 'GET':
		post_id = request.GET['postid']
	else:
		post_id = request.POST['postid']

	thumbsdown=0
	if post_id:
		p = Post.objects.get(id=int(post_id))
		if p:
			thumbsdown = p.thumbsdown + 1
			p.thumbsdown = thumbsdown
			p.save()
	return HttpResponse(thumbsdown)
