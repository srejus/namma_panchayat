from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    full_name = models.CharField(max_length=100)
    house_name = models.CharField(max_length=100)
    house_number = models.IntegerField(null=True,blank=True)
    pincode = models.CharField(max_length=6,null=True,blank=True)
    place = models.CharField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=15,null=True,blank=True)
    ward_no = models.IntegerField(null=True,blank=True)

    wallet = models.FloatField(default=0.0)
