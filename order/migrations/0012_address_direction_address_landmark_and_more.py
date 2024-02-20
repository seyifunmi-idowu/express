# Generated by Django 4.2.5 on 2024-02-20 17:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("order", "0011_alter_order_status")]

    operations = [
        migrations.AddField(
            model_name="address",
            name="direction",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="address",
            name="landmark",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="address",
            name="label",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="address",
            name="country",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="address",
            name="formatted_address",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="address", name="latitude", field=models.CharField(max_length=50)
        ),
        migrations.AlterField(
            model_name="address",
            name="longitude",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="address",
            name="meta_data",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="address",
            name="state",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
