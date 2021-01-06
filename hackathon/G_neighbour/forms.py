from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class DonationCardForm(ModelForm):
    class Meta:
        model = donation_card
        fields = ['title', 'content', 'location']


class EditProfileForm(ModelForm):
    class Meta:
        model = profile_description
        fields = ['description', 'first_name', 'last_name', 'location']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreateRequestForm(ModelForm):
    class Meta:
        model = request_card
        fields = ['title', 'content', 'location']


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class ReportForm(forms.Form):
    from_email = forms.EmailField(required=True)
    reported_user = forms.CharField(required=True)
    reason = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

class InformationPage(forms.Form):
    class Meta:
        model = information_page
        fields = ['title', 'content', ]

class EmergencyPage(forms.Form):
    class Meta:
        model = emergency_page
        fields = ['name', 'email', 'number']


class RateForm(forms.ModelForm):
    class Meta:
        model = user_rating
        fields = ['rating', 'comment']


class SendMessage(forms.ModelForm):
    class Meta:
        model = private_message
        fields = ['title','content']

