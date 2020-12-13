"""hackathon URL Configuration

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
from django.urls import path,include
from G_neighbour import views


urlpatterns = [
    path('',include('G_neighbour.urls')),
    path('admin/', admin.site.urls),
    #Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('home/', views.home, name='home'),
    path('banned/', views.ban, name='ban'),
    path('create/', views.createdonationcard, name='createdonationcard'),
    path('donations/', views.donations, name='donations'),
    path('completeddonations/', views.completeddonations, name='completeddonations'),
    path('cardcreation/', views.cardcreation, name='cardcreation' ),
    path('donations/<int:donation_pk>', views.viewdonation, name='viewdonation'),
    path('completeddonations/<int:donation_pk>)', views.viewcompleted, name='viewcompleted'),
    path('donations/<int:donation_pk>/complete', views.completedonation, name='completedonation'),
    path('donations/<int:donation_pk>/delete', views.deletedonation, name='deletedonation'),
]
