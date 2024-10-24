from django.db import models
from django.utils import timezone













  
  

  
from django.db import models
from datetime import date


# class Patient_Appointment(models.Model):
#     appointment_id = models.BigAutoField(primary_key=True)
#     patient = models.BigIntegerField(null=True, blank=True)  # Registered patient ID (optional for non-registered)
#     patient_name = models.CharField(max_length=30, null=True, blank=True)  # Non-registered patient's name
#     mobile_number = models.CharField(max_length=15, null=True, blank=True, unique=False)  # Non-registered patient's phone
#     email = models.EmailField(max_length=30, null=True, blank=True)  # Non-registered patient's email
#     doctor = models.ForeignKey(Staff_Allotment, on_delete=models.CASCADE, limit_choices_to={'is_doctor': True})
#     appointment_type = models.CharField(max_length=50, choices=[('Scheduled', 'Scheduled'), ('Queue', 'Queue')])
#     appointment_date = models.DateField()
#     from_time = models.TimeField()
#     to_time = models.TimeField()
#     notes = models.TextField(blank=True, null=True)
#     is_registered = models.BooleanField(default=False)  # Indicates if the patient is registered

#     def __str__(self):
#         return f"Appointment for {self.patient_name or 'Registered Patient ID: ' + str(self.patient)} with Dr. {self.doctor.username} on {self.appointment_date}"


# class Patient_Metadata(models.Model):
#     patient_id = models.BigAutoField(primary_key=True,db_column='patient_id')
#     patient_name = models.CharField(max_length=30, null=True)
#     mobile_number = models.CharField(max_length=15, unique=True)
#     email = models.EmailField(max_length=30, null=True, blank=True)
#     appointment_id = models.IntegerField(null=True, blank=True)
#     appointment_type = models.CharField(max_length=50, choices=[('Scheduled', 'Scheduled'), ('Queue', 'Queue')], null=True, blank=True)
#     appointment_date = models.DateField(null=True, blank=True)
#     from_time = models.TimeField(null=True, blank=True)
#     to_time = models.TimeField(null=True, blank=True)
#     notes = models.TextField(blank=True, null=True)
#     is_registered = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.patient_name} - Appointment on {self.appointment_date}"
  