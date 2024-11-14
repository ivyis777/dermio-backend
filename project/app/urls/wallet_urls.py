from django.urls import path
from app.controllers.wallet_controller import*


urlpatterns = [
    path("wallet_balance/",wallet_bal,name='wallet_balance'),


]