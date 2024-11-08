from django.urls import path
from app.controllers.staff_controller import *

urlpatterns = [
    path("get_all_staff_users_with_metadata/",get_all_staff_users_with_metadata ,name="get_all_staff_users_with_metadata"),
    path('pro/<str:profession>/', StaffMetaDataByDesignationView.as_view(), name='staff-meta-data-by-designation'),
    path('staff_meta/', StaffMetaDataUpdateOrCreateView.as_view(), name='create-staff-meta'),
    path('staff_meta/<int:staff_meta_id>/', staff_meta_data_create_or_update, name='update-staff-meta'),
    path('api/staff-by-department/<str:department>/', get_staff_by_department, name='get_staff_by_department'),
    path('check_availabity/', check_availability, name='check_doctor_availability'),
    path('top_doctorsc/', TopDoctorsListCreateAPIView.as_view(), name='top_doctors_list_create'),
    path('top_doctorsc/<int:top_doctor_id>/', TopDoctorsDetailAPIView.as_view(), name='top_doctors_detail'),
    path('top-doctors/', top_doctors_crud, name='top_doctors_create_list'),  # For create (POST) and list (GET)
    path('top-doctors/<int:top_doctor_id>/',top_doctors_crud, name='top_doctors_detail'),  # For retrieve (GET), update (PUT), delete (DELETE)


]   