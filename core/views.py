from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext, Context
from django.http import Http404, HttpResponse
from django.views.generic import View
# Auth Imports
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from braces.views import LoginRequiredMixin


class Home(View):
    def get(self, request):
        return render(request, 'home.html')


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


class CreateProfile(View):
    def get(self, request):
        return render(request, 'create_profile.html')


class LogoutView(View):
    """
    Logout View
    """

    def get(self, request):
        logout(request)
        return redirect("/")


class Dashboard(View):
    def get(self, request):
        members = User.objects.all()
        print(members)
        return render(request, "dashboard.html", {"members": members})


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
