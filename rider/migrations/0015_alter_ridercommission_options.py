# Generated by Django 4.2.5 on 2024-05-09 11:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("rider", "0014_commission_ridercommission_delete_guarantor")]

    operations = [
        migrations.AlterModelOptions(
            name="ridercommission",
            options={
                "get_latest_by": "created_at",
                "verbose_name": "rider to commission",
                "verbose_name_plural": "Rider to Commissions",
            },
        )
    ]
