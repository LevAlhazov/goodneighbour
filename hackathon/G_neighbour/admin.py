from django.contrib import admin
from .models import donation_card
# Register your models here.

class CardAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(donation_card, CardAdmin)