# Generated by Django 4.2.5 on 2023-09-30 10:10
from typing import List

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import helpers.db_helpers


class Migration(migrations.Migration):

    initial = True

    dependencies: List = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
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
                    "first_name",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=100,
                        null=True,
                        verbose_name="user first name",
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=100,
                        null=True,
                        verbose_name="user last name",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=100,
                        null=True,
                        unique=True,
                        verbose_name="User email address",
                    ),
                ),
                (
                    "email_verified",
                    models.BooleanField(
                        default=False, verbose_name="Email Verification Status"
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="phone number",
                    ),
                ),
                (
                    "phone_verified",
                    models.BooleanField(
                        default=False, verbose_name="Phone Number Verification Status"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "password",
                    models.CharField(
                        default=None, max_length=128, verbose_name="User password"
                    ),
                ),
                (
                    "avatar_url",
                    models.CharField(
                        blank=True, max_length=550, null=True, verbose_name="avatar url"
                    ),
                ),
                (
                    "street_address",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=100,
                        null=True,
                        verbose_name="User's street address",
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=100,
                        null=True,
                        verbose_name="User's city",
                    ),
                ),
                (
                    "state_of_residence",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=100,
                        null=True,
                        verbose_name="User's state of residence",
                    ),
                ),
                (
                    "country",
                    models.CharField(
                        blank=True,
                        default="Nigeria",
                        max_length=100,
                        null=True,
                        verbose_name="User's Country",
                    ),
                ),
                (
                    "bio",
                    models.TextField(
                        blank=True, default="", verbose_name="User short bio"
                    ),
                ),
                (
                    "user_type",
                    models.CharField(
                        choices=[
                            ("RIDER", "RIDER"),
                            ("CUSTOMER", "CUSTOMER"),
                            ("ADMIN", "ADMIN"),
                        ],
                        verbose_name="User type",
                    ),
                ),
                (
                    "date_of_birth",
                    models.DateField(
                        blank=True, null=True, verbose_name="Date of Birth"
                    ),
                ),
                (
                    "last_login_user_type",
                    models.CharField(
                        blank=True,
                        max_length=150,
                        null=True,
                        verbose_name="User's last user_type login",
                    ),
                ),
                (
                    "deactivated_reason",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="Why was this user deactivated?",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "db_table": "user",
            },
        ),
        migrations.CreateModel(
            name="UserActivity",
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
                    "category",
                    models.CharField(
                        max_length=100, verbose_name="User Activity Category"
                    ),
                ),
                (
                    "action",
                    models.CharField(
                        max_length=100, verbose_name="User Activity Action"
                    ),
                ),
                (
                    "context",
                    models.JSONField(
                        default=dict, null=True, verbose_name="User Activity Context"
                    ),
                ),
                (
                    "level",
                    models.CharField(
                        choices=[
                            ("ERROR", "ERROR"),
                            ("SUCCESS", "SUCCESS"),
                            ("INFO", "INFO"),
                            ("WARNING", "WARNING"),
                        ],
                        default="INFO",
                        max_length=100,
                        verbose_name="User Activity Level",
                    ),
                ),
                (
                    "session_id",
                    models.CharField(
                        blank=True,
                        max_length=60,
                        null=True,
                        verbose_name="User Activity Session Id",
                    ),
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
            ],
            options={
                "verbose_name": "user activity",
                "verbose_name_plural": "user activities",
                "db_table": "user_activity",
            },
        ),
    ]
