from django.contrib import admin
from .models import *


# Register your models here.
class WaterBillAdmin(admin.ModelAdmin):
    list_display = ['bill_amount','bill_created_at']

admin.site.register(WaterBills,WaterBillAdmin)
