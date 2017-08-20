from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext, Context
from django.http import Http404, HttpResponse
from django.views.generic import View
# Auth Imports
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from braces.views import LoginRequiredMixin

from core.models import *


class Home(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/directory/")
        return render(request, 'home.html')


class Directory(View):
    def get(self, request):
        members = User.objects.all()
        print(members)
        return render(request, "directory.html", {"members": members})


class Register(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            return HttpResponse("An account with this email already exists. Please log in if it's yours.")
        except:
            User.objects.create_user(first_name=fname,
                                     last_name=lname,
                                     email=email,
                                     username=username,
                                     password=password)
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_authenticated():
                    login(request, user)
                    return redirect('/profile/update')


class CreateProfile(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'create_profile.html')

    def post(self, request):
        about = request.POST['about']
        skills = request.POST['skills']
        collab = request.POST['collab']
        try:
            profile = Profile.objects.get(user=request.user)
            profile.about = about
            profile.skills = skills
            profile.open_for_collab = collab
            profile.save()
            return redirect("/directory/")
        except:
            profile = Profile(about=about, skills=skills,
                              open_for_collab=collab, user=request.user)
            profile.save()
            return redirect("/directory/")


class LogoutView(View):
    """
    Logout View
    """

    def get(self, request):
        logout(request)
        return redirect("/")


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_authenticated():
                    login(request, user)
                    return redirect('/dashboard/')
            else:
                return render(request, "login.html", {"msg": "Seems like you entered the wrong details."})
        except:
            return render(request, "login.html", {"msg": "Seems like you entered the wrong details."})
