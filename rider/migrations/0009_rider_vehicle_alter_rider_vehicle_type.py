# Generated by Django 4.2.5 on 2023-11-24 14:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0005_alter_vehicle_file_url"),
        ("rider", "0008_approvedrider_unapprovedrider"),
    ]

    operations = [
        migrations.AddField(
            model_name="rider",
            name="vehicle",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="order.vehicle",
                verbose_name="rider vehicle",
            ),
        ),
        migrations.AlterField(
            model_name="rider",
            name="vehicle_type",
            field=models.CharField(
                blank=True,
                max_length=30,
                null=True,
                verbose_name="rider's vehicle type",
            ),
        ),
    ]