# Generated by Django 4.2.5 on 2024-03-02 15:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import helpers.db_helpers


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("order", "0012_address_direction_address_landmark_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderTimeline",
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
                ("status", models.CharField(max_length=100)),
                ("proof_url", models.CharField(blank=True, max_length=550, null=True)),
                ("reason", models.CharField(blank=True, max_length=100, null=True)),
                ("meta_data", models.JSONField(blank=True, default=dict, null=True)),
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
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="customer_order",
                        to="order.order",
                        verbose_name="customer",
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
            ],
            options={
                "verbose_name": "Order Timeline",
                "verbose_name_plural": "Order Timelines",
                "db_table": "order_timeline",
            },
        )
    ]
