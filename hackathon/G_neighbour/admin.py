from django.contrib import admin

from .models import *
# Register your models here.


class CardAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

class InformationAdmin(admin.ModelAdmin):
    readonly_fields = ()

admin.site.register(donation_card, CardAdmin)
admin.site.register(request_card, CardAdmin)
admin.site.register(information_page, InformationAdmin)
admin.site.register(emergency_page, InformationAdmin)