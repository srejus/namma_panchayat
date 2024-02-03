from django.urls import path
from .views import *


urlpatterns = [
    path('manage',ManageWasteView.as_view()),
]