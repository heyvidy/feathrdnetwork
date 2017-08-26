# View imports
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext, Context
from django.http import Http404, HttpResponse
from django.views.generic import View
from braces.views import LoginRequiredMixin

# Auth Imports
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Model Imports
from core.models import *
import datetime


class Home(View):
    """
    Returns the home page.
    """

    def get(self, request):
        """
        Handles GET request for home view.
        """
        if request.user.is_authenticated:
            return redirect("/members/directory/")
        return render(request, 'home.html')


class Feed(LoginRequiredMixin, View):
    """
    View for the Progress Feed at /feed/progress/
    """

    def get(self, request):
        posts = Post.objects.all().order_by("-timestamp")
        return render(request, "feed.html", {"posts": posts})


class Directory(LoginRequiredMixin, View):
    """
    Returns the list of all memebers on the platform
    """

    def get(self, request):
        members = User.objects.all().order_by("id")
        print(members)
        return render(request, "directory.html", {"members": members})


class ProfilePage(LoginRequiredMixin, View):
    """
    Returns the Profile Page for each user.
    """

    def get(self, request, username):
        thisuser = User.objects.get(username=username)
        projects = Project.objects.filter(user=thisuser)
        posts = Post.objects.filter(user=thisuser).order_by('-timestamp')
        return render(request, "profile.html", {"thisuser": thisuser, "projects": projects, "posts": posts})


class Register(View):
    """
    Register page for users.
    """

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


class CreatePost(LoginRequiredMixin, View):
    """
    Handles POST request for creating a post in the profile page
    of each user
    """

    def post(self, request):
        body = request.POST['body']
        project_id = request.POST['project']
        project = Project.objects.get(pk=project_id)
        post = Post(body=body, project=project, user=request.user)
        post.save()
        return redirect("/{}/".format(request.user.username))


class CreateProfile(LoginRequiredMixin, View):
    """
    Handles Profile Creation Flow
    """

    def get(self, request):
        """
        returns the create profile form.
        """
        return render(request, 'create_profile.html')

    def post(self, request):
        """
        handles the post request from the form above.
        """
        about = request.POST['about']
        skills = request.POST['skills']
        collab = request.POST['collab']
        try:
            profile = Profile.objects.get(user=request.user)
            profile.about = about
            profile.skills = skills
            profile.open_for_collab = collab
            profile.save()
            return redirect("/members/directory/")
        except:
            profile = Profile(about=about, skills=skills,
                              open_for_collab=collab, user=request.user)
            profile.save()
            return redirect("/members/directory/")


class CreateProject(LoginRequiredMixin, View):
    """
    Handles Create Project Page.
    """

    def get(self, request):
        """
        returns create project form
        """
        return render(request, 'create_project.html')

    def post(self, request):
        title = request.POST['title']
        description = request.POST['about']
        url = request.POST['url']
        is_active = request.POST['is_active']
        user = request.user
        project = Project(title=title, about=description,
                          user=user, link=url, current=is_active)
        project.save()
        return redirect("/{}/".format(user.username))


class LogoutView(View):
    """
    Logout View
    """

    def get(self, request):
        logout(request)
        return redirect("/")


class LoginView(View):
    """
    Handles Login for users.
    """

    def get(self, request):
        """
        returns login page for users
        """
        return render(request, 'login.html')

    def post(self, request):
        """
        handles user info for login once submitted.
        """
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_authenticated():
                    login(request, user)
                    return redirect('/feed/progress/')
            else:
                return render(request, "login.html", {"msg": "Seems like you entered the wrong details."})
        except:
            return render(request, "login.html", {"msg": "Seems like you entered the wrong details."})
