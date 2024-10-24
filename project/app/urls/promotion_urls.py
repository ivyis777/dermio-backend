# urls.py
from django.urls import path
from app.controllers.promotion_controller import *

urlpatterns = [
    path('promotions/', promotions_list, name='promotions-list'),  # List and create promotions
    path('promotions/<int:promotion_id>/', promotions_detail, name='promotions-detail'),  # Get, update, delete promotion
]
