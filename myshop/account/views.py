from django.shortcuts import render,redirect
from django.contrib.auth.models import auth,User
from account.models import Profile
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse,JsonResponse
# Create your views here.
def login(req):
	if req.user.is_authenticated:
		return redirect("/home")
	if req.method =="POST":
		username=req.POST['username']
		passwd=req.POST['passwd']
		user=auth.authenticate(username=username,password=passwd)
		if user is not None:
			auth.login(req,user)
			return HttpResponse({"success":"success"})
		return JsonResponse({"error":"error"})
	return render(req,"account/login.html")
def logout(req):
	auth.logout(req)
	return redirect("/account/login")
def profile(req):
	if not req.user.is_authenticated:
		return render(req,"account/error.html",{"error":"Your are not login.! login to see your profile"})
	p=Profile.objects.get(user__username=req.user.username)
	return render(req,"account/profile.html",{"profile":p})

def signup(req):
	if req.user.is_authenticated:
		return redirect("/home")
	if req.method =="POST":
		name=req.POST['name']
		tel=req.POST['tel']
		email=req.POST['email']
		passwd=req.POST['passwd']
		security=req.POST['security']
		user=User.objects.create_user(username=name,password=passwd,email=email)
		Profile.objects.create(tel=tel,security=security,user=user)
		auth.login(req,user)
		return redirect('/home')	
	return render(req,"account/signup.html")
def forgot(req):
	return render(req,"account/forgot_password.html")