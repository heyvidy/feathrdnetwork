"""feathrd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from core.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Home.as_view()),
    url(r'^members/directory/$', Directory.as_view()),
    url(r'^(?P<username>[a-zA-Z]+)/$', ProfilePage.as_view()),
    url(r'^feed/progress/$', Feed.as_view()),
    url(r'^accounts/register/$', Register.as_view()),
    url(r'^accounts/login/$', LoginView.as_view()),
    url(r'^accounts/logout/$', LogoutView.as_view()),
    url(r'^profile/update/$', CreateProfile.as_view()),
    url(r'^post/create/$', CreatePost.as_view()),
    url(r'^project/create/$', CreateProject.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
