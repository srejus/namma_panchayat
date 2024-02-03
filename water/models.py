from django.db import models
from accounts.models import Account

# Create your models here.
class WaterBills(models.Model):
    user = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True,blank=True,related_name='water_bill_for')
    bill_created_by = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True,blank=True,
                                        related_name='water_bill_created_by')
    bill_amount = models.FloatField(default=0.0)
    usage = models.FloatField(default=0.0) # Ltr
    is_paid = models.BooleanField(default=False)
    note = models.TextField(null=True,blank=True)
    bill_created_at = models.DateTimeField(auto_now_add=True)
