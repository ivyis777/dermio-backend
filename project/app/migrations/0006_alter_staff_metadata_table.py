# Generated by Django 5.1 on 2024-10-29 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_slot_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='staff_metadata',
            table='dermio.staff_MetaData',
        ),
    ]
