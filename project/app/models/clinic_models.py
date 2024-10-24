from datetime import timezone
from django.db import models




class Clinic_Registration(models.Model):
    clinic_id = models.BigAutoField(primary_key=True)
    clinic_name = models.CharField(max_length=30, null=True,blank=True)
    clinic_mobile_number = models.CharField(max_length=15, null=True,blank=True)
    clinic_username=models.CharField(max_length=60,null=True,blank=True,unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=30, null=True,blank=True)
    mobile_number = models.CharField(max_length=15)   
    address = models.TextField(null=True,blank=True)
    #upload_logo = models.ImageField(upload_to="")
    
    def __str__(self):
        return f"{self.clinic_name} {self.clinic_id}"
    

class Branch_Create(models.Model):
    branch_id = models.BigAutoField(primary_key=True)
    clinic = models.ForeignKey(Clinic_Registration, on_delete=models.CASCADE,default=1)
    branch_name = models.CharField(max_length=100,unique=True) 
    # (branch_name) null=True, blank=True,default="Branch 1"
    # username = models.CharField(max_length=60, null=True, blank=True)
    password = models.CharField(max_length=10, null=False, blank=False)
    email = models.EmailField(max_length=30, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)


    def __str__(self):
        return f"{self.branch_name} {self.branch_id}"
 