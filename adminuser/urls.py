from django.urls import path
from .views import *

urlpatterns = [
    path('',AdminDashView.as_view()),
    path('water',AdminWaterView.as_view()),
    path('waste',AdminWasteView.as_view()),
    path('users',AdminUsersView.as_view()),
    path('users/approve/<int:id>',AdminApproveUserView.as_view()),
]