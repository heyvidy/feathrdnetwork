from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Profile models handles all basic info needed from Feathrd members.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    about = models.CharField(max_length=200, default="")
    skills = models.CharField(max_length=300, default="")
    open_for_collab = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


class Project(models.Model):
    """
    Project model is used to add Project info.
    """
    title = models.CharField(blank=False, max_length=100, default="Untitled")
    about = models.CharField(max_length=250, default="")
    link = models.CharField(max_length=250, default="#")
    timestamp = models.DateTimeField(auto_now=True)
    current = models.BooleanField(default=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return "{} by {}".format(self.title, self.user)


class Post(models.Model):
    """
    Post is an update about a project and each post
    is linked to project compulsorily. 
    """
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)

    def __str__(self):
        return "On {} on {}".format(self.project, self.timestamp)
