from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.utils import timezone

from accounts.models import Account
from .models import *


# Create your views here.
@method_decorator(login_required, name='dispatch')
class ManageWasteView(View):
    def get(self,request):
        collected_waste = WasteCollection.objects.filter(collected_from__user=request.user).order_by('-id')
        return render(request,'waste/manage_waste.html',{'collected_waste':collected_waste})
    


# waste collector related views
    
@method_decorator(login_required, name='dispatch')
class WCHomeView(View):
    def get(self,request):
        acc = Account.objects.get(user=request.user)
        if acc.user_type != 'WASTE_COLLECTOR':
            err = "You are not allowed to access this page!"
            return redirect(f"/?err={err}")
        
        houses = WasteCollection.objects.filter(collected_by=None)
        return render(request,'wc_home.html',{'houses':houses})
    

@method_decorator(login_required, name='dispatch')
class MarkWcView(View):
    def get(Self,request,id):
        waste = WasteCollection.objects.get(id=id)
        acc = Account.objects.get(user=request.user)

        current_datetime = timezone.now()
        waste.collected_by = acc
        waste.collected_at = current_datetime
        waste.save()
        return redirect("/waste/")