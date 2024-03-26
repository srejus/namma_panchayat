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
        if not water_bill:
            msg = "No water bill found!"
            return redirect(f"/?err={msg}")
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
    

# Water User Dashboard Section
    
@method_decorator(login_required, name='dispatch')
class WtrDashboardView(View):
    def get(self,request,id=None):
        acc = Account.objects.get(user=request.user)
        if acc.user_type != 'WATER_BILL_COLLECTOR':
            err = "You are not allowed to access this page!"
            return redirect(f"/?err={err}")  
        
        if id:
            return render(request,'wtr_bill_form.html',{'id':id})

        current_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        current_month_end = current_month_start.replace(month=current_month_start.month + 1, day=1) - timezone.timedelta(days=1)  
        bills = WaterBills.objects.filter(bill_created_at__range=(current_month_start,current_month_end)).values_list('user__id',flat=True)

        accs = Account.objects.exclude(id__in=bills)
        return render(request,'wtr_home.html',{'accs':accs})
    
    def post(self,request,id=None):
        amount = request.POST.get("amount")
        unit = request.POST.get("unit")
        notes = request.POST.get("notes")

        acc = Account.objects.get(user=request.user)
        usr = Account.objects.get(id=id)

        WaterBills.objects.create(user=usr,bill_created_by=acc,bill_amount=amount,usage=unit,note=notes)
        return redirect("/water/")