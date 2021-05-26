from django.contrib import admin
from .models import BillingProfile
#
# # Register your models here.
#
@admin.register(BillingProfile)
class BillingAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',
                    'email', 'city']
    # list_filter = ['available', 'created', 'updated','brand']
    # list_editable = ['price', 'available']
