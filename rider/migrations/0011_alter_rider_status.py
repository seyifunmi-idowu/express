# Generated by Django 4.2.5 on 2024-01-25 09:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("rider", "0010_alter_riderdocument_type")]

    operations = [
        migrations.AlterField(
            model_name="rider",
            name="status",
            field=models.CharField(
                choices=[
                    ("APPROVED", "APPROVED"),
                    ("UNAPPROVED", "UNAPPROVED"),
                    ("DISAPPROVED", "DISAPPROVED"),
                    ("SUSPENDED", "SUSPENDED"),
                ],
                default="UNAPPROVED",
                max_length=30,
                verbose_name="Rider workspace status",
            ),
        )
    ]
