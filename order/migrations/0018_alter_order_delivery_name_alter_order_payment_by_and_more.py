# Generated by Django 4.2.5 on 2024-06-03 14:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("order", "0017_alter_vehicle_status")]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="delivery_name",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Delivery address"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="payment_by",
            field=models.CharField(
                blank=True,
                choices=[("RECIPIENT", "Recipient"), ("SENDER", "Sender")],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="pickup_name",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Pickup address"
            ),
        ),
    ]
