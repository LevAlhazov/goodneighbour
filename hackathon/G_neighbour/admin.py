from django.contrib import admin

from .models import *
# Register your models here.


class CardAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(donation_card, CardAdmin)