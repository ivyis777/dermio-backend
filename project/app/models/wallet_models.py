from django.db import models
from app.models.patient_models import Patient

class wallet(models.Model):
    wallet_id=models.BigAutoField(primary_key=True)
    patient_id=models.ForeignKey(Patient,on_delete=models.CASCADE,to_field='id',db_column='to_user_id', db_constraint=False,null=True,blank=True)
    wallet_bal=models.DecimalField(max_digits=10, decimal_places=2)
    email=models.ForeignKey(Patient,on_delete=models.CASCADE,to_field='email',db_column='email', db_constraint=False,null=True,blank=True, related_name="wallet user email+")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=False,null=True)
    updated_by = models.CharField(max_length=40, unique=True,null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'wallet'




class wallet_transactions_debit(models.Model):
    transaction_id=models.BigAutoField(primary_key=True)
    patient_id=models.ForeignKey(Patient,on_delete=models.CASCADE,to_field='id',db_column='to_patient_id', db_constraint=False,null=True,blank=True)
    date_time=models.DateTimeField()
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    is_debit=models.BooleanField(default=True)
    to=models.CharField(max_length=40,db_column='to')
    current_bal=models.DecimalField(max_digits=10, decimal_places=2,default=0.00) 
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=False,null=True)
    updated_by = models.CharField(max_length=40, unique=True,null=True)
    is_active = models.BooleanField(default=True)


    class   Meta:
        managed = True
        db_table='wallet_transacation_debit'

class wallet_transactions_credit(models.Model):
    transaction_id=models.BigAutoField(primary_key=True)
    date_time=models.DateTimeField()
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    is_received=models.BooleanField()
    to=models.CharField(max_length=40,db_column='to')
    to_user_id=models.ForeignKey(Patient,on_delete=models.CASCADE,to_field='id',db_column='to_user_id', db_constraint=False,null=True,blank=True)
    from_username=models.CharField(max_length=50,db_column='from_username')

    is_from=models.CharField(max_length=50,db_column='from')
    current_bal=models.DecimalField(max_digits=10, decimal_places=2,default=0.00) 



    class Meta:
        managed = True

        db_table='wallet_transacation_credit'
