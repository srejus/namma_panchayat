from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q

from .models import *

# Create your views here.
class LoginView(View):
    def get(self,request):
        err = request.GET.get("err")
        type_ = request.GET.get("type","user")
        if type_ == 'user':
            login_text = "Login as User"
        elif type_ == 'wc':
            login_text = "Login as Waste Collector"
        elif type_ == 'wtr':
            login_text = "Login as Water Bill Collector"

        return render(request,'login.html',{'err':err,'login_text':login_text})

    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        type_ = request.GET.get("type","user")

        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            acc = Account.objects.get(user=user)
            if type_ == 'user' and acc.user_type != 'USER':
                err = "Invalid USER credentails!"
                return redirect(f"/accounts/login/?err={err}")
            
            if type_ == 'wc' and acc.user_type != 'WASTE_COLLECTOR':
                err = "Invalid WASTE_COLLECTOR credentails!"
                return redirect(f"/accounts/login/?err={err}")
            
        
            if type_ == 'wtr' and acc.user_type != 'WATER_BILL_COLLECTOR':
                err = "Invalid USER credentails!"
                return redirect(f"/accounts/login/?err={err}")
            
            
            login(request, user)
            return redirect("/")
        err = "Invalid credentails!"
        return redirect(f"/accounts/login/?err={err}")
    

class SignupView(View):
    def get(self,request):
        err = request.GET.get("err")
        return render(request,'signup.html',{'err':err})

    def post(self,request):
        username = request.POST.get("username")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        house_name = request.POST.get("house_name")
        house_number = request.POST.get("house_number")
        ward_number = request.POST.get("ward_number")
        place = request.POST.get("place")
        pincode = request.POST.get("pincode")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            err = "Password not matching!"
            return redirect(f"/accounts/signup?err={err}")
        
        user = User.objects.filter(username=username)
        if user.exists():
            err = "User with this username already exists"
            return redirect(f"/accounts/signup?err={err}")
        
        acc = Account.objects.filter(Q(house_number=house_number) | Q(phone=phone)).exists()
        if acc:
            err = "User with this phone or house_number already exists"
            return redirect(f"/accounts/signup?err={err}")
        
        user = User.objects.create_user(username=username,email=email,password=password)
        acc = Account.objects.create(user=user,full_name=name,phone=phone,
                                     house_name=house_name,place=place,pincode=pincode,
                                     house_number=house_number,ward_no=ward_number)

        return redirect('/accounts/login')
    

class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect("/accounts/login/")    
        
    

