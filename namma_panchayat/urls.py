from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('',include('home.urls')),
    path('waste/',include('waste.urls')),
    path('water/',include('water.urls')),
    path('adminuser/',include('adminuser.urls')),
]
