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
from django.core.paginator import Paginator
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django import template


# ---------------------------------------------------------------------------------------------------------------------#
### buttons ###

def index(request):
    return render(request, 'index.html')

def NotAutho(request):
    return render(request,'NotAuthorized.html')


def cardcreation(request):
    return render(request, 'cardcreation.html')


def ban(request):
    return render(request, 'ban.html')


def logoutuser(request):
    if request.method == 'GET':
        logout(request)
        return redirect('index')
    else:
        return redirect('index')


### user- donations ###
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


@allowed_user(allowed_roles=["Donators", ])
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


### admin ###
def adminViewCompletedDonations(request):
    u_donations = donation_card.objects.filter(datecompleted__isnull=False)
    return render(request, 'adminViewCompletedDonations.html', {'u_donations': u_donations})


### user - requests ###
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
            return render(request, 'viewcompletedrequests.html',
                          {'u_request': u_request, 'form': form, 'error': 'Bad entry'})


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


### General - all surfers ###

def generaldonations(request):
    u_donations = donation_card.objects.all()
    return render(request, 'generaldonations.html', {'u_donations': u_donations})


def splitbylocation(request, cat_pk):
    u_donations = donation_card.objects.all()
    category = get_object_or_404(location_model, location=cat_pk)
    cat_list = []
    for u_donation in u_donations:
        if u_donation.location == category:
            cat_list.append(u_donation)
    return render(request, 'splitbylocation.html', {'cat_list': cat_list})


def generalrequests(request):
    u_requests = request_card.objects.all()
    return render(request, 'generalrequests.html', {'u_requests': u_requests})


def informationpage(request):
    a_informations = information_page.objects.all()
    return render(request, 'informationpage.html', {'a_informations': a_informations})


def emergencypage(request):
    u_emers = emergency_page.objects.all()
    return render(request, 'emergencypage.html', {'u_emers': u_emers})


def userprofile(request):
    current_user = request.user
    return render(request, 'userprofile.html', {'current_user': current_user})


def viewprofile(request, request_pk):
    u_request = get_object_or_404(profile_description, pk=request_pk)
    if request.method == 'GET':
        return render(request, 'viewprofile.html', {'u_request': u_request})
    else:
        try:
            return redirect('donations')
        except ValueError:
            return render(request, 'viewprofile.html', {'u_request': u_request})


### chat messaging ###
def mymessages(request):
    user = request.user
    u_messages = private_message.objects.all()
    message_list = []
    for x in u_messages:
        if x.receiver == user:
            message_list.append(x)
    return render(request, 'mymessages.html', {'message_list': message_list})


def sentmessages(request):
    user = request.user
    u_messages = private_message.objects.all()
    message_list = []
    for x in u_messages:
        if x.sender == user:
            message_list.append(x)
    return render(request, 'sentmessages.html', {'message_list': message_list})


### admin - to send messages from admin to user ###
def adminusercontact(request):
    all_users = User.objects.all()
    paginator = Paginator(all_users, 6)
    page = request.GET.get('page', 1)
    users = paginator.page(page)
    return render(request, 'adminusercontact.html', {'all_users': all_users, 'users': users})


### sorting requests ###
def requestbycategory(request, cat_pk):
    u_requests = request_card.objects.all()
    cat_list = []
    for x in u_requests:
        if x.category == cat_pk:
            cat_list.append(x)
    return render(request, 'requestbycategory.html', {'cat_list': cat_list})


### conversation between users ###
def conversation(request, user_pk):
    user1 = request.user
    u_messages = private_message.objects.filter(receiver=user1)
    user2 = get_object_or_404(User, pk=user_pk)
    message_list = []
    for x in u_messages:
        if x.sender == user2:
            message_list.append(x)
    return render(request, 'conversation.html', {'message_list': message_list})


### ratings ###
def myrating(request):
    current_user = request.user
    ratings = user_rating.objects.all()
    all_users = User.objects.filter(groups__name__in=['Donators'])
    count = 0
    sum = 0
    rating_average = 0
    for x in ratings:
        if x.user.id == current_user.id:
            sum = sum + x.rating
            count += 1
    if count != 0:
        rating_average = sum / count
    your_rating = 0
    avg_list = {}
    for y in all_users:
        count = 0
        user_sum = 0
        for z in ratings:
            if y.id == z.user.id and current_user.id != y.id:
                user_sum += z.rating
                count += 1
        if count != 0:
            avg_list[y] = user_sum / count
    for x in avg_list.values():
        if x > rating_average:
            your_rating += 1
    your_rating += 1
    sorted_dict = {}
    sorted_keys = sorted(avg_list, key=avg_list.get)
    for w in sorted_keys:
        sorted_dict[w] = avg_list[w]
    sorted_dict = sorted_dict.items()
    sorted_dict = tuple(sorted_dict)
    return render(request, 'myrating.html', {'your_rating': your_rating, 'rating_average': rating_average,
                                             'avg_list': sorted_dict})


@allowed_user(allowed_roles=["Receiver"])
def ratingforreceivers(request):
    ratings = user_rating.objects.all()
    all_users = User.objects.filter(groups__name__in=['Donators'])
    avg_list = {}
    for y in all_users:
        count = 0
        user_sum = 0
        for z in ratings:
            if y.id == z.user.id:
                user_sum += z.rating
                count += 1
        if count != 0:
            avg_list[y] = user_sum / count
    sorted_dict = {}
    sorted_keys = sorted(avg_list, key=avg_list.get)
    for w in sorted_keys:
        sorted_dict[w] = avg_list[w]
    sorted_dict = sorted_dict.items()
    sorted_dict = tuple(sorted_dict)
    return render(request, 'ratingforreceivers.html', {'avg_list': sorted_dict, 'name_list': sorted_keys})
# ---------------------------------------------------------------------------------------------------------------------#
### functionality


@unauthenticated_user
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signupuser.html', {'form': CreateUserForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], email=request.POST['email'],
                                                password=request.POST['password1'])
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


### contact - admin ###
@allowed_user(allowed_roles=["Donators","Receiver"])
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
                send_mail(subject, message, from_email, ['lev_alk@hotmail.com'], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "contact.html", {'form': form})


### report to admin ###
@allowed_user(allowed_roles=["Donators","Receiver"])
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


### Donators Profile ###
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


### rating ###
def rateuser(request, user_pk):
    user2 = get_object_or_404(User, pk=user_pk)
    ratings = user_rating.objects.all()
    count = 0
    sum = 0
    rating_average = 0
    user_comment = []
    for z in ratings:
        if z.user.id == user2.id:
            user_comment.append(z.comment)

    for x in ratings:
        if x.user.id == user2.id:
            sum = sum + x.rating
            count += 1
    if count != 0:
        rating_average = sum / count

    user_counter = 0
    for y in ratings:
        if y.user.id == user2.id:
            user_counter += 1
    if user_counter > 1:
        return render(request, 'rateuser.html', {'rating_average': rating_average, 'user_comment': user_comment})
    user_tracker = request.user
    if user2 == user_tracker:
        return render(request, 'rateuser.html', {'rating_average': rating_average, 'user_comment': user_comment})
    else:
        form = RateForm()
        if request.method == 'POST':
            form.user = user2
            form = RateForm(request.POST)
            if form.is_valid():
                newrate = form.save(commit=False)
                newrate.user = user2
                newrate.save()
                return redirect('index')
    return render(request, 'rateuser.html',
                  {'form': form, 'rating_average': rating_average, 'user_comment': user_comment})


### Users "chat" ###
@allowed_user(allowed_roles=["Donators","Receiver"])
def sendmessage(request, user_pk):
    user = request.user
    user2 = get_object_or_404(User, pk=user_pk)
    form = SendMessage()
    if request.method == 'POST':
        form.sender = user
        form.receiver = user2
        form = SendMessage(request.POST)
        if form.is_valid():
            new_msg = form.save(commit=False)
            new_msg.receiver = user2
            new_msg.sender = user
            new_msg.save()
            return redirect('index')
    return render(request, 'sendmessage.html', {'form': form})
# ---------------------------------------------------------------------------------------------------------------------#
