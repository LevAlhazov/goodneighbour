from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import DonationCardForm, CreateUserForm
from .models import *
from .decorators import unauthenticated_user, allowed_user
from django.contrib.auth.models import Group
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django import template


# Create your views here.
def index(request):
    return render(request, 'index.html')


# DELETE IF NOT NEEDED?!@ (ALSO URL AND HTML)
# def home(request):
#     u_donations = donation_card.objects.all()
#     Users = User.objects.all()
#     context = { 'donations': u_donations, 'Users':Users}
#     return render(request,'home.html')


def cardcreation(request):
    return render(request, 'cardcreation.html')


def ban(request):
    return render(request, 'ban.html')


@unauthenticated_user
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signupuser.html', {'form': CreateUserForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                given_type = int(request.POST.get('usertype'))
                if given_type == 1:
                    group = Group.objects.get(name='Donators')
                    user.groups.add(group)
                if given_type == 2:
                    group = Group.objects.get(name='Receiver')
                    user.groups.add(group)
                login(request, user)
                return redirect('index')

            except IntegrityError:
                return render(request, 'signupuser.html',
                              {'form': CreateUserForm(), 'error': 'The user already exists, please try again'})
        else:
            return render(request, 'signupuser.html',
                          {'form': CreateUserForm(), 'error': 'Passwords did not match, please try again'})
        # Passwords don't match.


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'loginuser.html', {'form': AuthenticationForm(),
                                                      'error': 'Username or password did not match, please try again'})
        else:
            login(request, user)
            return redirect('index')


def logoutuser(request):
    if request.method == 'GET':
        logout(request)
        return redirect('index')
    else:
        return redirect('index')


@allowed_user(allowed_roles=["Donators"])
def createdonationcard(request):
    if request.method == 'GET':
        return render(request, 'createdonationcard.html', {'form': DonationCardForm()})
    else:
        try:
            form = DonationCardForm(request.POST)
            newcard = form.save(commit=False)
            newcard.user = request.user
            newcard.save()
            return redirect('donations')
        except ValueError:
            return render(request, 'createdonationcard.html', {'form': DonationCardForm(), 'error': 'Bad Data entered'})


@allowed_user(allowed_roles=["Donators"])
def donations(request):
    u_donations = donation_card.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'donations.html', {'u_donations': u_donations})


@allowed_user(allowed_roles=["Donators"])
def completeddonations(request):
    u_donations = donation_card.objects.filter(user=request.user, datecompleted__isnull=False)
    return render(request, 'completeddonations.html', {'u_donations': u_donations})


@allowed_user(allowed_roles=["Donators"])
def viewdonation(request, donation_pk):
    u_donation = get_object_or_404(donation_card, pk=donation_pk)
    if request.method == 'GET':
        form = DonationCardForm(instance=u_donation)
        return render(request, 'viewdonation.html', {'u_donation': u_donation, 'form': form})
    else:
        try:
            form = DonationCardForm(request.POST, instance=u_donation)
            form.save()
            return redirect('donations')
        except ValueError:
            return render(request, 'viewdonation.html', {'u_donation': u_donation, 'form': form, 'error': 'Bad entry'})


@allowed_user(allowed_roles=["Donators"])
def viewcompleted(request, donation_pk):
    u_donation = get_object_or_404(donation_card, pk=donation_pk)
    if request.method == 'GET':
        form = DonationCardForm(instance=u_donation)
        return render(request, 'viewcompleted.html', {'u_donation': u_donation, 'form': form})
    else:
        try:
            form = DonationCardForm(request.POST, instance=u_donation)
            form.save()
            return redirect('completeddonations')
        except ValueError:
            return render(request, 'viewcompleted.html', {'u_donation': u_donation, 'form': form, 'error': 'Bad entry'})


@allowed_user(allowed_roles=["Donators"])
def completedonation(request, donation_pk):
    u_donation = get_object_or_404(donation_card, pk=donation_pk, user=request.user)
    if request.method == 'POST':
        u_donation.datecompleted = timezone.now()
        u_donation.save()
        return redirect('donations')


@allowed_user(allowed_roles=["Donators"])
def deletedonation(request, donation_pk):
    u_donation = get_object_or_404(donation_card, pk=donation_pk, user=request.user)
    if request.method == 'POST':
        u_donation.delete()
        return redirect('donations')

def information(request):
    return render(request, 'information.html')

def officialbodies(request):
    return render(request, 'officialbodies.html')