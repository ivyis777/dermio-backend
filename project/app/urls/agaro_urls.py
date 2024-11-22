from django.urls import path
from app.controllers.agaro_controller import *

urlpatterns = [
    path('generate-token/', generate_agora_token, name='generate_agora_token')
]