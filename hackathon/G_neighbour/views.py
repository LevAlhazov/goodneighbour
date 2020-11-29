from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

# Create your views here.

def index(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')

def ban(request):
    return render(request,'ban.html')

def signupuser(request):
    if request.method=='GET':
        return render(request, 'signupuser.html' , {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')

            except IntegrityError:
                return render(request, 'signupuser.html', {'form': UserCreationForm(), 'error': 'The user already exists'})
        else:
            return render(request, 'signupuser.html' , {'form':UserCreationForm(), 'error':'Passwords did not match'})
            # Passwords don't match.

def loginuser(request):
    if request.method=='GET':
        return render(request, 'loginuser.html' , {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'loginuser.html', {'form': AuthenticationForm(), 'error':'Username or password did not match'})
        else:
            login(request, user)
            return redirect('home')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

