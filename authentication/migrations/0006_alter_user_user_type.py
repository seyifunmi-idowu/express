# Generated by Django 4.2.5 on 2024-03-20 19:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("authentication", "0005_user_referral_code_referraluser")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                choices=[
                    ("RIDER", "RIDER"),
                    ("CUSTOMER", "CUSTOMER"),
                    ("BUSINESS", "BUSINESS"),
                    ("ADMIN", "ADMIN"),
                ],
                verbose_name="User type",
            ),
        )
    ]