from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.models import Group




class location_model(models.Model):
    location = models.CharField(max_length=150)

    def __str__(self):
        return self.location

    @staticmethod
    def get_locations():
        return location_model.objects.all()


class donation_card(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    # Stores the relationship between a donation card and a user
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    location = models.ForeignKey(location_model, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class request_card(models.Model):
    category_tup = ((1,'מוצרי מזון'),(2,'מוצרי היגיינה'),(3,'ציוד משרדי'),(4,'הלבשה'),(5,'מוצרי תינוקות'))
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    # Stores the relationship between a donation card and a user
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    location = models.ForeignKey(location_model, null=True, on_delete=models.CASCADE)
    category = models.PositiveSmallIntegerField(choices=category_tup)

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



class profile_description(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    location = models.ForeignKey(location_model, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    def __str__(self):
        return str(self.user)


class user_rating(models.Model):
    rate = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'))
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=rate)
    comment = models.TextField(max_length=255)


class private_message(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    title = models.CharField(max_length=150, default="new message")
    created_at = models.DateTimeField(auto_now_add=True)