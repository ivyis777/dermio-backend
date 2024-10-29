# from datetime import timezone
from datetime import timedelta
from django.db import models
# from datetime import date
from django.utils import timezone




class user_otp(models.Model):
    user_email=models.CharField(max_length=60)
    otp=models.CharField(max_length=4)
    created_at = models.DateTimeField(default=timezone.now)
    delete_at = models.DateTimeField(default=timezone.now)
    purpose=models.CharField(max_length=15)
    is_resend=models.BooleanField(default=False,null=True,blank=True)
    resend_count = models.IntegerField(default=0)