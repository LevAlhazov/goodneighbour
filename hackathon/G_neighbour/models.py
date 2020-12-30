from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.models import Group



class donation_card(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    # Stores the relationship between a donation card and a user
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class request_card(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    # Stores the relationship between a donation card and a user
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class information_page(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title

class emergency_page(models.Model):
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    number = models.CharField(max_length=150)

    def __str__(self):
        return self.name
