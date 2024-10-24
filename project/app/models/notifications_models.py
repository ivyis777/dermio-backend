from django.db import models
from app.models.patient_models import Patient



class Notification(models.Model):
    user_id=models.ForeignKey(Patient,on_delete=models.CASCADE,to_field='id',db_column='user_id', db_constraint=False,null=True,blank=True)
    title = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=False,null=True)
    updated_by = models.CharField(max_length=40, unique=True,null=True)
    is_active = models.BooleanField(default=True)

    def _str_(self):
        return self.title