from django.urls import path
from . views import *

urlpatterns = [
    path('pay-bill',WaterBillView.as_view()),
]