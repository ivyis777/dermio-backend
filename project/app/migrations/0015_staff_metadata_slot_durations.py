# Generated by Django 5.1 on 2024-11-08 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_alter_patient_image_alter_staff_metadata_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff_metadata',
            name='slot_durations',
            field=models.JSONField(blank=True, null=True),
        ),
    ]