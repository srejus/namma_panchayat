from django.urls import path
from .views import *


urlpatterns = [
    path('manage',ManageWasteView.as_view()),
    path('',WCHomeView.as_view()),
    path('mark-as-collected/<int:id>',MarkWcView.as_view()),
]