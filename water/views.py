from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import WaterBills


# Create your views here.
@method_decorator(login_required, name='dispatch')
class WaterBillView(View):
    def get(self,request):
        water_bills = WaterBills.objects.filter(user__user=request.user).order_by('-id')
        return render(request,'water/water_home.html',{'water_bills':water_bills})
