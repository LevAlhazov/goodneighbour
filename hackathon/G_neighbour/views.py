from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import *
from .decorators import unauthenticated_user, allowed_user
from django.contrib.auth.models import Group
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
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
                user = User.objects.create_user(request.POST['username'], email=request.POST['email'], password=request.POST['password1'])
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


@allowed_user(allowed_roles=["Donators", "Admin"])
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


def adminViewCompletedDonations(request):
    u_donations = donation_card.objects.filter(datecompleted__isnull=False)
    return render(request, 'adminViewCompletedDonations.html', {'u_donations': u_donations})


@allowed_user(allowed_roles=["Donators"])
def deletedonation(request, donation_pk):
    u_donation = get_object_or_404(donation_card, pk=donation_pk, user=request.user)
    if request.method == 'POST':
        u_donation.delete()
        return redirect('donations')


@allowed_user(allowed_roles=["Receiver"])
def createrequest(request):
    if request.method == 'GET':
        return render(request, 'createrequest.html', {'form': CreateRequestForm()})
    else:
        try:
            form = CreateRequestForm(request.POST)
            newcard = form.save(commit=False)
            newcard.user = request.user
            newcard.save()
            return redirect('requests')
        except ValueError:
            return render(request, 'createrequest.html', {'form': CreateRequestForm(), 'error': 'Bad Data entered'})


@allowed_user(allowed_roles=["Receiver"])
def completedrequests(request):
    u_requests = request_card.objects.filter(user=request.user, datecompleted__isnull=False)
    return render(request, 'completedrequests.html', {'u_requests': u_requests})


@allowed_user(allowed_roles=["Receiver"])
def viewcompletedrequests(request, request_pk):
    u_request = get_object_or_404(request_card, pk=request_pk)
    if request.method == 'GET':
        form = CreateRequestForm(instance=u_request)
        return render(request, 'viewcompletedrequests.html', {'u_request': u_request, 'form': form})
    else:
        try:
            form = CreateRequestForm(request.POST, instance=u_request)
            form.save()
            return redirect('viewcompletedrequests')
        except ValueError:
            return render(request, 'viewcompletedrequests.html', {'u_request': u_request, 'form': form, 'error': 'Bad entry'})


@allowed_user(allowed_roles=["Receiver"])
def requests(request):
    u_requests = request_card.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'requests.html', {'u_requests': u_requests})


@allowed_user(allowed_roles=["Receiver"])
def viewrequest(request, request_pk):
    u_request = get_object_or_404(request_card, pk=request_pk)
    if request.method == 'GET':
        form = CreateRequestForm(instance=u_request)
        return render(request, 'viewrequest.html', {'u_request': u_request, 'form': form})
    else:
        try:
            form = CreateRequestForm(request.POST, instance=u_request)
            form.save()
            return redirect('requests')
        except ValueError:
            return render(request, 'viewrequest.html', {'u_request': u_request, 'form': form, 'error': 'Bad entry'})


@allowed_user(allowed_roles=["Receiver"])
def completerequest(request, request_pk):
    u_request = get_object_or_404(request_card, pk=request_pk, user=request.user)
    if request.method == 'POST':
        u_request.datecompleted = timezone.now()
        u_request.save()
        return redirect('requests')


@allowed_user(allowed_roles=["Receiver"])
def deleterequest(request, request_pk):
    u_request = get_object_or_404(request_card, pk=request_pk, user=request.user)
    if request.method == 'POST':
        u_request.delete()
        return redirect('requests')


def generaldonations(request):
    u_donations = donation_card.objects.all()
    return render(request, 'generaldonations.html', {'u_donations': u_donations })


def splitbylocation(request, cat_pk):
    u_donations = donation_card.objects.all()
    print(u_donations)
    category = get_object_or_404(location_model, location=cat_pk)
    cat_list = []
    for u_donation in u_donations:
        if u_donation.location == category:
            cat_list.append(u_donation)
    return render(request, 'splitbylocation.html', {'cat_list': cat_list})




def generalrequests(request):
    u_requests = request_card.objects.all()
    return render(request, 'generalrequests.html', {'u_requests': u_requests })


def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['lev_alk@hotmail.com'],fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "contact.html", {'form': form})


def successView(request):
    return render(request, "index.html")


def reportView(request):
    if request.method == 'GET':
        form = ReportForm()
    else:
        form = ReportForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            reported_user = form.cleaned_data['reported_user']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(reason, reported_user, from_email, ['lev_alk@hotmail.com'])
                send_mail(reported_user, message, from_email, ['lev_alk@hotmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "report.html", {'form': form})


def informationpage(request):
    a_informations = information_page.objects.all()
    return render(request, 'informationpage.html', {'a_informations': a_informations})


def emergencypage(request):
    u_emers = emergency_page.objects.all()
    return render(request, 'emergencypage.html', {'u_emers': u_emers })


def userprofile(request):
    current_user = request.user
    return render(request, 'userprofile.html', {'current_user': current_user})


def edituserprofile(request):
    current_user = request.user
    if request.method == 'GET':
        form = CreateUserForm(instance=current_user)
        return render(request, 'edituserprofile.html', {'current_user': current_user, 'form': form})
    else:
        try:
            form = CreateUserForm(request.POST, instance=current_user)
            form.save()
            return redirect('userprofile')
        except ValueError:
            return render(request, 'userprofile.html',
                          {'current_user': current_user, 'form': form, 'error': 'Bad entry'})


def edituserdata(request):
    current_user = request.user
    if request.method == 'GET':
        form = EditProfileForm(instance=current_user)
        return render(request, 'userdata.html', {'current_user': current_user, 'form': form})
    else:
        try:
            form = EditProfileForm(request.POST, instance=current_user)
            form.save()
            return redirect('userprofile')
        except ValueError:
            return render(request, 'userprofile.html',
                          {'current_user': current_user, 'form': form, 'error': 'Bad entry'})


def createprofile(request):
    if request.method == 'GET':
        return render(request, 'createuserprofile.html', {'form': EditProfileForm()})
    else:
        try:
            form = EditProfileForm(request.POST)
            newcard = form.save(commit=False)
            newcard.user = request.user
            newcard.save()
            return redirect('userprofile')
        except ValueError:
            return render(request, 'createuserprofile.html', {'form': EditProfileForm(), 'error': 'Bad Data entered'})


def viewprofile(request, request_pk):
    u_request = get_object_or_404(profile_description, pk=request_pk)
    if request.method == 'GET':
        return render(request, 'viewprofile.html', {'u_request': u_request})
    else:
        try:
            return redirect('donations')
        except ValueError:
            return render(request, 'viewprofile.html', {'u_request': u_request})