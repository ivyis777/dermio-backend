from django.urls import path
from app.controllers.email_controller import signup_otp
# from app.controllers.patient_controller import 
from app.controllers.clinic_controller import *
from app.views import *

from app.controllers.patient_controller import *

from app.controllers.email_controller import *
# from app





urlpatterns = [

    path("clinic_reg/", clinic_reg, name="clinic_reg"),
    path("update_clinic/", update_clinic, name="update_clinic"),
    path("get_clinic_data/<int:clinic_id>/",get_clinic_data, name="get_clinic_data"),
    path("clinic_login/", clinic_login, name="clinic_login"),
    
    path("create_branch/", create_branch, name="create_branch"),
    path("update_branch/", update_branch, name="update_branch"),
    path("get_branch_data/<int:branch_id>/",get_branch_data, name="get_branch_data"),
    path("get_all_branches/", get_all_branches, name="get_all_branches"),
    path("branch_login/", branch_login, name="branch_login"),
        
    path("send_signin_otp/",send_signin_otp ,name="send_signin_otp"),
    # path("resend_signin_otp/",resend_signin_otp ,name="resend_signin_otp"),    
    # path("user_signIn/",user_signIn ,name="user_signIn"),
    
    # path("send_registration_otp/",send_registration_otp ,name="send_registration_otp"),
    # path("resend_registration_otp/",resend_registration_otp ,name="resend_registration_otp"),
    # path('user_reg/', user_reg, name='user_reg'),
    # path("update_user_reg/", update_user_reg, name="update_user_reg"),
    
    
    # path("get_doctor_profiles/",get_doctor_profiles ,name="get_doctor_profiles"),
    # path("get_all_staff_users_with_metadata/",get_all_staff_users_with_metadata ,name="get_all_staff_users_with_metadata"),
    
    path("registerPatientNow/",registerPatientNow ,name="registerPatientNow"),
    path("update_patient_details/",update_patient_details ,name="update_patient_details"),
    
    path('get_patient/<int:patient_id>/', get_patient, name='get_patient'),
    path("list_patients/",list_patients ,name="list_patients"),
    path('delete_patient/<int:patient_id>/', delete_patient, name='delete_patient'),
    
    
    path("schedule_appointment/",schedule_appointment ,name="schedule_appointment"),
    path("rebook_appointment/",rebook_appointment ,name="rebook_appointment"),
    path("get_appointments/",get_appointments ,name="get_appointments"),
    path('signup_otp/',signup_otp, name='send_email'),

    

        
]        