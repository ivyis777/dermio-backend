from django.db import models
from django.core.exceptions import ValidationError

# from app.model.quiz import QuizMetaData

class Promotions(models.Model):
    promotion_id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=200)
    image = models.ImageField(upload_to='app.images/', null=True, blank=True)  # Add this line for the image field
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=False,null=True)
    updated_by = models.CharField(max_length=40, unique=True,null=True)
    is_active = models.BooleanField(default=True)


class Coupons(models.Model):
    coupon_id = models.AutoField(primary_key=True)
    coupon_code = models.CharField(max_length=6, unique=True)
    valid_from = models.DateField(null=True)
    valid_till = models.DateField(null=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=False,null=True)
    updated_by = models.CharField(max_length=40, unique=True)
    is_active = models.BooleanField(default=True)

    def clean(self):
        # Validate that percentage is between 0 and 100
        if self.percentage < 0 or self.percentage > 100:
            raise ValidationError('Percentage must be between 0 and 100.')
        
        # Validate that valid_till is greater than or equal to valid_from
        if self.valid_till and self.valid_from and self.valid_till < self.valid_from:
            raise ValidationError('valid_till must be greater than or equal to valid_from.')

    def save(self, *args, **kwargs):
        self.clean()
        super(Coupons, self).save(*args, **kwargs)

    def __str__(self):
        return self.coupon_code

class Coupon_claimed(models.Model):
    claim_id=models.AutoField(primary_key=True)
    coupon_id = models.ForeignKey('Coupons',to_field='coupon_id',db_column='coupon_id', related_name='coupon', on_delete=models.CASCADE)
    user_id=models.BigIntegerField(db_column='user_id',null=True,blank=True)
    quiz_id=models.BigIntegerField(db_column='quiz_id',null=True,blank=True)
    amount_claimed=models.IntegerField(db_column='amount',null=True,blank=True)
    