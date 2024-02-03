from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from accounts.models import Account
from .models import *


# Create your views here.
@method_decorator(login_required, name='dispatch')
class ManageWasteView(View):
    def get(self,request):
        collected_waste = WasteCollection.objects.filter(collected_from__user=request.user).order_by('-id')
        return render(request,'waste/manage_waste.html',{'collected_waste':collected_waste})