"""forumApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from forumSozluk import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index),
    path('login',views.login),
    path('logout',views.logout),
    path('register',views.register),
    path('forgot-password',views.forgot_password),
    path('profile/<username>',views.profile),
    path('settings/<username>', views.mysettings),
    path('code-verification',views.verification),
    path('change-password',views.changePassword),
    path('trends',views.trends),
    path('create-post',views.createPost),
    path('like',views.like),
    path('post/<postID>', views.details),
    path('namechange', views.nameChange),
    path('fullnamechange', views.fullnamechange),
    path('emailchange', views.emailchange),
    path('passwordchange', views.passwordchange),
    path('categories', views.categories),
    path('categories/<category>', views.selectcategory),
    path('search', views.search,name="search"),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
