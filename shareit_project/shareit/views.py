from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from shareit.models import UserProfile
from shareit.models import UserForm, UserProfileForm
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from shareit.models import Category, Post, Rating

def home(request):
	template = loader.get_template('shareit/home.html')
	cat_list = Category.objects.all()
	posts_list=Post.objects.all()
	
	for cat in cat_list:
                cat_name = cat.name
	context = RequestContext(request, { 'posts_list':posts_list,'cat_list': cat_list})
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
			registered = True
		else:
			print uform.errors, pform.errors
	else:
		uform = UserForm()
		pform = UserProfileForm()
	return render_to_response('shareit/register.html', {'uform':uform, 'pform':pform, 'registered':registered}, context)

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
def followers(request):
	return HttpResponse('Since you are an authenticated user, you can view your followers.')

@login_required
def following(request):
	return HttpResponse('Since you are an authenticated user, you can view users you are followers.')

@login_required
def user_logout(request):
	context = RequestContext(request)
	logout(request)
	return HttpResponseRedirect('/shareit/')

@login_required
def user_profiles(request, name):
        cat_list = Category.objects.all()
        if not request.user.is_authenticated():
                HttpResponseRedirect('/login/')
        userSearched=User.objects.get(username=name)
        p=UserProfile.objects.get(user=userSearched)
        picture=p.picture
        context = RequestContext(request,{ 'picture':picture,'user1': userSearched, 'cat_list': cat_list})
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
