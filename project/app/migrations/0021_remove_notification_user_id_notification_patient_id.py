# Generated by Django 5.1 on 2024-11-15 12:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_wallet_transactions_credit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='user_id',
        ),
        migrations.AddField(
            model_name='notification',
            name='patient_id',
            field=models.ForeignKey(blank=True, db_column='patient_id', db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]