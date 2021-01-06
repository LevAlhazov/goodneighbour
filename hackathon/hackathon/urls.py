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
from django.urls import path, include
from G_neighbour import views
from G_neighbour.views import *
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy




urlpatterns = [
    path('', include('G_neighbour.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    # Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),
    # path('home/', views.home, name='home'),
    path('banned/', views.ban, name='ban'),
    path('create/', views.createdonationcard, name='createdonationcard'),

    # donation model
    path('donations/', views.donations, name='donations'),
    path('completeddonations/', views.completeddonations, name='completeddonations'),
    path('cardcreation/', views.cardcreation, name='cardcreation'),
    path('completeddonations/<int:donation_pk>', views.viewcompleted, name='viewcompleted'),
    path('donations/<int:donation_pk>', views.viewdonation, name='viewdonation'),
    path('donations/<int:donation_pk>/complete', views.completedonation, name='completedonation'),
    path('donations/<int:donation_pk>/delete', views.deletedonation, name='deletedonation'),

    # request model
    path('requests/', views.requests, name='requests'),
    path('createrequest/', views.createrequest, name='createrequest'),
    path('completedrequests/', views.completedrequests, name='completedrequests'),
    path('completedrequests/<int:request_pk>', views.viewcompletedrequests, name='viewcompletedrequests'),
    path('requests/<int:request_pk>', views.viewrequest, name='viewrequest'),
    path('requests/<int:request_pk>/completereq', views.completerequest, name='completerequest'),
    path('requests/<int:request_pk>/deletereq', views.deleterequest, name='deleterequest'),


    # display
    path('generaldonations/', views.generaldonations, name='generaldonations'),
    path('generalrequests/', views.generalrequests, name='generalrequests'),
    path('splitbylocation/<str:cat_pk>/', views.splitbylocation, name='splitbylocation'),

    # information and contact
    path('contact/', views.contactView, name='contact'),
    path('success/', views.successView, name='success'),
    path('report/', views.reportView, name='report'),
    path('informationpage/', views.informationpage, name='informationpage'),
    path('emergencypage/', views.emergencypage, name='emergencypage'),

    # profile and messaging
    path('userprofile/', views.userprofile, name='userprofile'),
    path('edituserprofile/', views.edituserprofile, name='edituserprofile'),
    path('userdata/', views.edituserdata, name='edit_profile_data'),
    path('createprofile/',views.createprofile, name='create_profile'),
    path('userprofile/<int:request_pk>', views.viewprofile, name='viewprofile'),
    path('sendmessage/<int:user_pk>', views.sendmessage, name='sendmessage'),
    path('mymessages/', views.mymessages, name='mymessages'),
    path('sentmessages/', views.sentmessages, name='sentmessages'),
    path('conversation/<int:user_pk>', views.conversation, name='conversation'),


    #rating and comments
    path('rateuser/<int:user_pk>', views.rateuser, name='rateuser'),
    path('myrating/', views.myrating, name='myrating'),
    path('ratingforreceivers/', views.ratingforreceivers, name='ratingforreceivers'),


    # admin data
    path('adminViewCompletedDonations/', views.adminViewCompletedDonations, name='adminViewCompletedDonations')

]
