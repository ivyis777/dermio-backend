from datetime import timezone
from django.db import models
from app.models.clinic_models import Clinic_Registration,Branch_Create

class Doctor_Departments(models.Model):
    dept_id = models.BigAutoField(primary_key=True)
    dept_name=models.CharField(max_length=30,db_column='dept_name',unique=True)








class Staff_Allotment(models.Model):
    staff_id = models.BigAutoField(primary_key=True)
    clinic_id = models.ForeignKey(Clinic_Registration, on_delete=models.CASCADE, null=True, blank=True,default=1)
    branch_id = models.ForeignKey(Branch_Create, on_delete=models.CASCADE, null=True, blank=True,default=1)
    username = models.CharField(max_length=50, unique=True)  # Added unique constraint for usernames
    is_admin = models.BooleanField(default=False) 
    is_doctor = models.BooleanField(default=False)
    is_receptionist = models.BooleanField(default=False)
    is_nurse = models.BooleanField(default=False)
    is_pharmacist = models.BooleanField(default=False)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=30)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=False,null=True)
    updated_by = models.CharField(max_length=40, unique=True,null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.username}"   


class Leave_Management(models.Model):
    leave_id=models.BigAutoField(primary_key=True)
    staff_id=models.ForeignKey(Staff_Allotment,on_delete=models.CASCADE,to_field='staff_id',db_column='doctor_id')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()


class Days(models.Model):
    day_id=models.BigAutoField(primary_key=True,db_column="day_id")
    day = models.CharField(max_length=10)


class slots_booked(models.Model):
    slot_id=models.BigAutoField(primary_key=True,db_column="slot_id")
    doctor_id=models.ForeignKey(Staff_Allotment,on_delete=models.CASCADE,to_field='staff_id',db_column='doctor_id')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=False,null=True)
    updated_by = models.CharField(max_length=40, unique=True,null=True)
    is_active = models.BooleanField(default=True)
    








class Slot(models.Model):
    
    slot_id= models.BigAutoField(primary_key=True)

    doctor = models.ForeignKey(Staff_Allotment, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=False)
    on_leave=models.BooleanField(default=False)

    class Meta:
        db_table="slots"

class Staff_MetaData(models.Model):
    staff_meta_id = models.BigAutoField(primary_key=True,unique=True)
    staff_id=models.ForeignKey(Staff_Allotment,on_delete=models.CASCADE,to_field='staff_id',db_column='staff_id')
    name = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=30, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.IntegerField(default=30, null=True, blank=True)
    registration_number = models.CharField(max_length=20, null=True, blank=True)
    consulting_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    permanent_address = models.TextField(null=True, blank=True)
    speciality = models.CharField(max_length=100, null=True, blank=True) 
    designation = models.CharField(max_length=100, null=True, blank=True)
    profession = models.CharField(max_length=30, null=True, blank=True)
    department=models.CharField(max_length=30, null=True, blank=True)
    image = models.ImageField(upload_to='staff_images/', null=True, blank=True)  # Add this line for the image field
    slot_duration = models.IntegerField(default=30)  # Slot duration in minutes
    # start_time = models.TimeField()  # e.g., 9:00 AM
    # end_time = models.TimeField()
    Fullname_IMC=models.CharField(max_length=300,null=True)
    IMC_Reg_No=models.CharField(max_length=300,null=True)
    Days=models.TextField(db_column='Days' ,null=True,blank=True)



    class Meta:
        db_table="staff_MetaData"
    

class Top_doctors(models.Model):
    top_doctor_id=models.BigAutoField(primary_key=True)
    doctor_id=models.ForeignKey(Staff_Allotment,on_delete=models.CASCADE,to_field='staff_id',db_column='doctor_id')
    department=models.ForeignKey(Doctor_Departments,on_delete=models.CASCADE,db_column='dept_name',to_field='dept_name',null=True)
    image = models.ImageField(upload_to='app.images/', null=True, blank=True)  # Add this line for the image field
    
