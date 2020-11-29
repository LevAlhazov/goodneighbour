from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login

# Create your views here.

def index(request):
    return render(request,'index.html')

def signupuser(request):
    if request.method=='GET':
        return render(request, 'signupuser.html' , {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('index')


            except IntegrityError:
                return render(request, 'signupuser.html', {'form': UserCreationForm(), 'error': 'The user already exists'})
        else:
            return render(request, 'signupuser.html' , {'form':UserCreationForm(), 'error':'Passwords did not match'})
            # Passwords don't match.



