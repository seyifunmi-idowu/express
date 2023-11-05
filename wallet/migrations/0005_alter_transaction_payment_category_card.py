# Generated by Django 4.2.5 on 2023-11-05 15:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import helpers.db_helpers


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("wallet", "0004_alter_transaction_object_class_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="payment_category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("FUND_WALLET", "Fund wallet"),
                    ("CUSTOMER_PAY_RIDER", "Customer pays rider"),
                    ("RIDER_PAY_CUSTOMER", "Rider pays customer"),
                    ("WITHDRAW", "Withdrawal"),
                ],
                max_length=255,
                null=True,
            ),
        ),
        migrations.CreateModel(
            name="Card",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=helpers.db_helpers.generate_id,
                        editable=False,
                        max_length=60,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "deleted_at",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[("ACTIVE", "ACTIVE"), ("DELETED", "DELETED")],
                        default="ACTIVE",
                        max_length=20,
                    ),
                ),
                ("card_type", models.CharField(blank=True, max_length=30, null=True)),
                ("card_auth", models.CharField(blank=True, max_length=30, null=True)),
                ("last_4", models.CharField(blank=True, max_length=30, null=True)),
                ("exp_month", models.CharField(blank=True, max_length=30, null=True)),
                ("exp_year", models.CharField(blank=True, max_length=30, null=True)),
                (
                    "country_code",
                    models.CharField(blank=True, max_length=30, null=True),
                ),
                ("brand", models.CharField(blank=True, max_length=30, null=True)),
                ("first_name", models.CharField(blank=True, max_length=50, null=True)),
                ("last_name", models.CharField(blank=True, max_length=50, null=True)),
                ("reusable", models.BooleanField(default=True)),
                (
                    "customer_code",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="created by",
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="deleted by",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="updated by",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_card",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-created_at"], "abstract": False},
        ),
    ]
