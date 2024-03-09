from django.urls import path
from . views import *

urlpatterns = [
    path('bills',WaterBillView.as_view()),
    path('pay',PayBillView.as_view()),

    path('',WtrDashboardView.as_view()),
    path('<int:id>',WtrDashboardView.as_view()),
]