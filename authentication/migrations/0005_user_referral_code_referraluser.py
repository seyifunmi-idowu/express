# Generated by Django 4.2.5 on 2024-02-16 00:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import helpers.db_helpers


class Migration(migrations.Migration):
    dependencies = [("authentication", "0004_user_receive_email_promotions")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="referral_code",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.CreateModel(
            name="ReferralUser",
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
                    "referral_code",
                    models.CharField(blank=True, max_length=30, null=True),
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
                    "referred_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="referred_users",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Referred By",
                    ),
                ),
                (
                    "referred_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="referral_users",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Referred User",
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
                "verbose_name": "referral user",
                "verbose_name_plural": "referral users",
                "db_table": "referral_user",
            },
        ),
    ]
