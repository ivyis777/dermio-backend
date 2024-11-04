from django.urls import path
from app.controllers.staff_controller import *

urlpatterns = [
    path("get_all_staff_users_with_metadata/",get_all_staff_users_with_metadata ,name="get_all_staff_users_with_metadata"),
    path('pro/<str:profession>/', StaffMetaDataByDesignationView.as_view(), name='staff-meta-data-by-designation'),
    path('top-doctors/', TopDoctorsListView.as_view(), name='top-doctors-list'),
    path('staff_meta/', StaffMetaDataUpdateOrCreateView.as_view(), name='create-staff-meta'),
    path('staff_meta/<int:staff_meta_id>/', StaffMetaDataUpdateOrCreateView.as_view(), name='update-staff-meta'),
    path('api/staff-by-department/<str:dep2artment>/', get_staff_by_department, name='get_staff_by_department'),
    path('check_availabity/', check_availability, name='check_doctor_availability'),


]