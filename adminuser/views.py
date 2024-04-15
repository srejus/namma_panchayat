from django.shortcuts import render,redirect
from django.views import View

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from accounts.models import *
from waste.models import *
from water.models import *
from .models import *


# Create your views here.
@method_decorator(login_required, name='dispatch')
class AdminDashView(View):
    def get(self,request):
        if not request.user.is_superuser:
            err = "You don't have access to this page!"
            return redirect(f"/?err={err}")
        
        return render(request,'admin/home.html')
    

@method_decorator(login_required, name='dispatch')
class AdminWaterView(View):
    def get(self,request):
        if not request.user.is_superuser:
            err = "You don't have access to this page!"
            return redirect(f"/?err={err}")
        
        water_bills = WaterBills.objects.all().order_by('-id')
        return render(request,'admin/water.html',{'water_bills':water_bills})
    

@method_decorator(login_required, name='dispatch')
class AdminWasteView(View):
    def get(self,request):
        if not request.user.is_superuser:
            err = "You don't have access to this page!"
            return redirect(f"/?err={err}")
        
        collected_waste = WasteCollection.objects.all().order_by('-id')
        return render(request,'admin/waste.html',{'collected_waste':collected_waste})
    

@method_decorator(login_required, name='dispatch')
class AdminUsersView(View):
    def get(self,request):
        if not request.user.is_superuser:
            err = "You don't have access to this page!"
            return redirect(f"/?err={err}")
        
        users = Account.objects.all().order_by('-id')
        return render(request,'admin/users.html',{'users':users})
    

@method_decorator(login_required, name='dispatch')
class AdminApproveUserView(View):
    def get(self,request,id):
        if not request.user.is_superuser:
            err = "You don't have access to this page!"
            return redirect(f"/?err={err}")
        
        acc = Account.objects.get(id=id)
        acc.user.is_active= True
        acc.user.save()
        return redirect("/adminuser/users")
    


@method_decorator(login_required,name='dispatch')
class AdminNotificationView(View):
    def get(self,request,id=None):
        if id:
            Notification.objects.get(id=id).delete()
            return redirect("/adminuser/notifications")

        notifications = Notification.objects.all().order_by('-id')
        return render(request,'admin/notifications.html',{'notifications':notifications})
    

class AdminAddNotificationView(View):
    def get(self,request):
        return render(request,'admin/add_notifications.html')
    
    def post(self,request):
        title = request.POST.get("title")
        Notification.objects.create(title=title)
        return redirect("/adminuser/notifications")