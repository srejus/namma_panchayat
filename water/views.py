from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone

from .models import WaterBills
from accounts.models import Account


# Create your views here.
@method_decorator(login_required, name='dispatch')
class WaterBillView(View):
    def get(self,request):
        water_bills = WaterBills.objects.filter(user__user=request.user).order_by('-id')
        return render(request,'water/water_home.html',{'water_bills':water_bills})


@method_decorator(login_required, name='dispatch')
class PayBillView(View):
    def get(self,request):
        current_datetime = timezone.now()
        water_bill = WaterBills.objects.filter(
            bill_created_at__year=current_datetime.year,
            bill_created_at__month=current_datetime.month,user__user=request.user,is_paid=False
        ).last()
        acc = Account.objects.get(user=request.user)
        if acc.wallet >= water_bill.bill_amount:
            water_bill.is_paid = True
            acc.wallet -= water_bill.bill_amount
            acc.save()
            water_bill.save()
            err = "Water Bill Payment Successfull!"
            # send noti to the user about the bill paid
        else:
            err = "Insufficient Wallet Balance to Pay the Bill!"
        
        return redirect(f"/?err={err}")