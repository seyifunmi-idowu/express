# Generated by Django 4.2.5 on 2023-11-19 10:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("wallet", "0008_rename_payee_transaction_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="transaction_user",
                to=settings.AUTH_USER_MODEL,
            ),
        )
    ]
