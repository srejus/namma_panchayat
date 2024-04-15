from django.shortcuts import render,redirect
from django.views import View

from django.utils import timezone
from datetime import datetime

from waste.models import WasteCollection
from water.models import WaterBills
from accounts.models import Account

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from namma_panchayat.utils import *

# Create your views here.
class IndexView(View):
    def get(self,request):
        # Get the first day of the current month
        if request.user.is_authenticated:
            current_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

            # Get the last day of the current month
            current_month_end = current_month_start.replace(month=current_month_start.month + 1, day=1) - timezone.timedelta(days=1)

            # Query objects created in the current month
            has_waste = WasteCollection.objects.filter(
                collected_from__user=request.user,created_at__range=(current_month_start, current_month_end)).exists()
            acc = Account.objects.get(user=request.user)
            if acc.user_type == 'WASTE_COLLECTOR':
                return redirect("/waste/")
            elif acc.user_type == 'WATER_BILL_COLLECTOR':
                return redirect("/water/")
            
            wallet = acc.wallet
              # water bill fetching section
            current_datetime = timezone.now()

            water_bill = WaterBills.objects.filter(
                bill_created_at__year=current_datetime.year,
                bill_created_at__month=current_datetime.month,user__user=request.user,is_paid=False
            ).last()
        else:
            wallet = "0.0"
            has_waste = False
            water_bill = None

      
        err = request.GET.get("err")
        return render(request,'index.html',{'has_waste':has_waste,"wallet":wallet,'water_bill':water_bill,'err':err})


class MarkWasteView(View):
    def get(self,request):
        acc = Account.objects.get(user=request.user)
        if acc.wallet >= 50:
            is_paid = True
            acc.wallet -= 50
            acc.save()
            
        else:
            is_paid = False
        
        if acc.wallet <= 50:
            subject = "Wallet balance Low!"
            msg = f"Hello {acc.full_name},\n\nYour wallet balance is low. Please recharge immediately\n\nThanks"

            if acc.user.email:
                send_mail(acc.user.email,subject,msg)

        WasteCollection.objects.create(collected_from=acc,no_of_sacks=1,is_paid=is_paid) # get this no of sacks and populate this field
        return redirect("/")
    

@method_decorator(login_required,name='dispatch')
class RechargeView(View):
    def get(self,request):
        return render(request,'recharge.html')
    
    def post(self,request):
        amount = request.POST.get("amount")
        pay_url = create_stripe_payment_link(amount)

        if pay_url:
            acc = Account.objects.get(user=request.user)
            acc.wallet += float(amount)
            acc.save()
            return redirect(pay_url)
        
        err = "Failed to create payment url!"
        return redirect(f"/?err={err}")