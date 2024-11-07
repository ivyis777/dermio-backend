from datetime import timezone
from django.db import models
from app.models.Staff_models import Staff_Allotment,Slot





class Book_Appointment(models.Model):
    appointment_id=models.BigAutoField(primary_key=True)
    doctor_id=models.ForeignKey(Staff_Allotment,on_delete=models.CASCADE,to_field='staff_id',db_column='doctor_id')
    appointment_date=models.DateField(db_column="appointment date",null=True)
    slot_id=models.ForeignKey(Slot,on_delete=models.CASCADE,to_field='slot_id',db_column='slot_id')
    age=models.IntegerField(db_column="age")
    blood_group=models.CharField(max_length=4,db_column='blood group',blank=True, null=True)
    relation=models.CharField(max_length=15,db_column='relation',blank=True, null=True)
    description=models.CharField(max_length=500,db_column='description',blank=True, null=True)
    symptoms=models.CharField(max_length=100,db_column='symptoms',blank=True, null=True)
    total_amount=models.IntegerField(db_column="total amount")
    coupon_used=models.BooleanField(default=False)
    coupon_amount=models.IntegerField(db_column="coupon_amount",default=0)
    net_payable=models.IntegerField(db_column="net payable",default=0)
    is_self=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=False,null=True)
    updated_by = models.CharField(max_length=40, unique=True,null=True)
    is_active = models.BooleanField(default=True)

    


class Spotted_Images(models.Model):
    image_id=models.BigAutoField(primary_key=True)
    Appointment_id=models.BigIntegerField(db_column="Appointment_id")
    spotted_place=models.CharField(max_length=50,db_column='symptom',blank=True, null=True)
    image_1=models.ImageField(upload_to='patient_images/') 
    image_2=models.ImageField(upload_to='patient_images/')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=False,null=True)
    updated_by = models.CharField(max_length=40, unique=True,null=True)
    is_active = models.BooleanField(default=True)







class Patient_Symptoms(models.Model):
    symptom_id=models.BigAutoField(primary_key=True)
    symptom_name=models.CharField(max_length=50,db_column='symptom',blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=False,null=True)
    updated_by = models.CharField(max_length=40, unique=True,null=True)
    is_active = models.BooleanField(default=True)
    

import os
import uuid
from django.db import models

def patient_image_path(instance, filename):
    # Generate a unique filename using UUID only
    unique_id = uuid.uuid4()
    extension = filename.split('.')[-1]  # Extract the original file extension

    # Filename based solely on UUID and file extension
    new_filename = f"{instance.id}_{unique_id}.{extension}"
    return os.path.join("patients", new_filename)


class Patient(models.Model):


    id = models.BigAutoField(primary_key=True)
    company_id=models.IntegerField(default=1,blank=True,db_column='company_id')
    branch_id=models.IntegerField(default=1,blank=True)
    username = models.CharField(unique= True, db_column='username', max_length=50, blank=True, null=True)  # Field name made lowercase.

    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='gender', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=50, blank=True, null=True)  # Field name made lowercase.
    age=models.IntegerField(db_column="age",blank=True,null=True)
    dob=models.DateField(db_column="dob",blank=True,null=True)


    mobile = models.CharField(unique=True, max_length=15, blank=True, null=True)
    email = models.CharField(unique=True, max_length=50, blank=True, null=True)
    pincode = models.IntegerField(db_column='pincode',blank=True, null=True)
    
    registeredat = models.DateTimeField(db_column='registeredAt')  # Field name made lowercase.
    lastlogin = models.DateTimeField(db_column='lastLogin', blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(max_length=50,db_column='city', blank=True, null=True)
    country = models.CharField(max_length=50,db_column='country',blank=True, null=True)
    state=models.CharField(max_length=50,db_column='state',blank=True, null=True)
    image = models.ImageField(upload_to=patient_image_path, null=True, blank=True)  # Add this line for the image field
    # is_creator=models.BooleanField(default=False)

    through_google=models.BooleanField(db_column="through_google", default=False)
    
    fcm_token = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    updated_at=models.DateTimeField(db_column='updated_at', blank=True, null=True,auto_now=True)
    updated_by=models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        managed = True
        db_table = 'patient'


    @property
    def is_anonymous(self):
        """
        Always return False. Required by Django's authentication system.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True for authenticated users. Required by Django's authentication system.
        """
        return True

    def has_perm(self, perm, obj=None):
        """
        Required for handling permissions in the Django admin.
        You can implement more complex logic here if needed.
        """
        return True

    def has_module_perms(self, app_label):
        """
        Required for handling permissions in the Django admin.
        You can implement more complex logic here if needed.
        """
        return True

    

class Patient_Registration(models.Model):
    patient_id = models.CharField(max_length=10,primary_key=True,unique=True)
    branch_id = models.BigIntegerField(null=True, default=True)
    clinic_id = models.BigIntegerField(null=True, default=True)
    patient_name = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=30, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=30, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    patient_type = models.CharField(max_length=10, null=True, blank=True, choices=[('Regular', 'Regular'), ('EHS', 'EHS')])
    is_registered = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.patient_id} {self.patient_name}"
    
   
    def save(self, *args, **kwargs):
        if not self.patient_id:
            last_patient = Patient_Registration.objects.order_by('patient_id').last()

            # Check if last patient_id exists and is formatted as "SERXXX"
            if last_patient and isinstance(last_patient.patient_id, str) and last_patient.patient_id.startswith('SER'):
                last_code = int(last_patient.patient_id[3:])  # Extract numeric part after "SER"
                new_code = last_code + 1
            else:
                new_code = 1  # Start from 1 if no previous patient exists

            self.patient_id = f"SER{new_code:03d}"  # Format as "SERXXX", e.g., "SER001"

        super().save(*args, **kwargs)




class Patient_Appointment(models.Model):
    appointment_id = models.BigAutoField(primary_key=True)
    patient = models.CharField(max_length=10, null=True, blank=True)  # Store patient_id as string
    patient_name = models.CharField(max_length=30, null=True, blank=True)  # Non-registered patient's name
    mobile_number = models.CharField(max_length=15, null=True, blank=True, unique=False)  # Non-registered patient's phone
    email = models.EmailField(max_length=30, null=True, blank=True)  # Non-registered patient's email
    doctor = models.ForeignKey(Staff_Allotment, on_delete=models.CASCADE, limit_choices_to={'is_doctor': True})
    appointment_type = models.CharField(max_length=50, choices=[('Scheduled', 'Scheduled'), ('Queue', 'Queue')])
    appointment_date = models.DateField()
    from_time = models.TimeField()
    to_time = models.TimeField()
    notes = models.TextField(blank=True, null=True)
    is_registered = models.BooleanField(default=False)  # Indicates if the patient is registered

    def __str__(self):
        return f"Appointment for {self.patient_name or 'Registered Patient ID: ' + str(self.patient)} with Dr. {self.doctor.username} on {self.appointment_date}"
