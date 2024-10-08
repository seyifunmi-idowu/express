# Generated by Django 4.2.5 on 2024-02-10 22:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("order", "0009_order_paid_alter_order_status")]

    operations = [
        migrations.AddField(
            model_name="order",
            name="fele_amount",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name="order",
            name="paid_fele",
            field=models.BooleanField(default=False),
        ),
    ]
