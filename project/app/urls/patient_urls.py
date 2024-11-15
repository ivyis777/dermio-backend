from django.urls import path


from app.controllers.patient_controller import *
from app.controllers.email_controller import *



urlpatterns = [
    path("send_otp/",send_otp,name='send_otp'),
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('get_profile_page/', get_profile_page, name='get-user-update') ,

    path('update_profile_page/', update_profile_page, name='user-update'),
    
    path('appointments/', BookAppointmentList.as_view(), name='appointment-list'),
    path('appointments/<int:pk>/', BookAppointmentDetail.as_view(), name='appointment-detail'),

    path('symptoms/', symptom_list, name='symptom_list'),
    path('symptoms/<int:pk>/', symptom_detail, name='symptom_detail'),

    path('verify-coupon/', VerifyCoupon.as_view(), name='verify-coupon'),

]
