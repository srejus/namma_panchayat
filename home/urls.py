from django.urls import path
from .views import *

urlpatterns = [
    path('',IndexView.as_view()),
    path('mark-waste-availability',MarkWasteView.as_view()),

    path('recharge',RechargeView.as_view()),
]