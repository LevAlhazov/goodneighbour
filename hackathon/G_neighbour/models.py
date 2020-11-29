from django.db import models
from django.contrib.auth.models import User

class donation_card(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    # Stores the relationship between a donation card and a user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

