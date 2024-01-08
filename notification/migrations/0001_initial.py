# Generated by Django 4.2.5 on 2023-12-23 07:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import helpers.db_helpers


class Migration(migrations.Migration):
    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="UserNotification",
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
                (
                    "one_signal_id",
                    models.CharField(max_length=100, verbose_name="one_signal id"),
                ),
                (
                    "external_id",
                    models.CharField(max_length=100, verbose_name="external id"),
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
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_notification",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "User Notifications",
                "verbose_name_plural": "User Notifications",
                "db_table": "user_notification",
            },
        )
    ]