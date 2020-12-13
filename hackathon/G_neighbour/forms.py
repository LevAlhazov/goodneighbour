from django.forms import ModelForm
from .models import donation_card
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class DonationCardForm(ModelForm):
    class Meta:
        model = donation_card
        fields = ['title', 'content']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
