from django.db import models

from accounts.models import Account

# Create your models here.
class WasteCollection(models.Model):
    collected_from = models.ForeignKey(Account,on_delete=models.SET_NULL,
                                       null=True,blank=True,related_name='waste_collected_from')
    collected_by = models.ForeignKey(Account,on_delete=models.SET_NULL,
                                       null=True,blank=True,related_name='waste_collected_by')
    
    no_of_sacks = models.IntegerField(default=1)
    is_paid = models.BooleanField(default=False)
    collected_at = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.collected_from)+" - "+str(self.no_of_sacks)
