from django.shortcuts import render,redirect
from django.views import View

from django.utils import timezone
from datetime import datetime

from waste.models import WasteCollection
from accounts.models import Account


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
            wallet = Account.objects.get(user=request.user).wallet
        else:
            wallet = "0.0"
            has_waste = False
        return render(request,'index.html',{'has_waste':has_waste,"wallet":wallet})


class MarkWasteView(View):
    def get(self,request):
        acc = Account.objects.get(user=request.user)
        if acc.wallet >= 50:
            is_paid = True
            acc.wallet -= 50
            acc.save()
        else:
            is_paid = False

        WasteCollection.objects.create(collected_from=acc,no_of_sacks=1,is_paid=is_paid) # get this no of sacks and populate this field
        return redirect("/")