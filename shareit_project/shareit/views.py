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
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))

def category(request):
	template = loader.get_template('shareit/category.html')
	cat_list = Category.objects.all()
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
def user_profile(request):
        if not request.user.is_authenticated():
                HttpResponseRedirect('/login/')
        user = request.user.get_profile
        context = RequestContext(request,{ 'user': user})
        return render_to_response('shareit/profile.html', {}, context)
