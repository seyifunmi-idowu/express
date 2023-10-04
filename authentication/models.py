from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from authentication.managers import UserManager
from feleexpress import settings
from helpers.db_helpers import BaseAbstractModel

# Create your models here.


class User(BaseAbstractModel, AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model
    """

    USER_TYPE_CHOICES = [
        ("RIDER", "RIDER"),
        ("CUSTOMER", "CUSTOMER"),
        ("ADMIN", "ADMIN"),
    ]

    first_name = models.CharField(
        max_length=100,
        verbose_name="user first name",
        null=True,
        blank=True,
        default=None,
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name="user last name",
        null=True,
        blank=True,
        default=None,
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        verbose_name="User email address",
        blank=True,
        null=True,
    )
    email_verified = models.BooleanField("Email Verification Status", default=False)
    phone_number = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="phone number"
    )
    phone_verified = models.BooleanField(
        "Phone Number Verification Status", default=False
    )
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    password = models.CharField(
        verbose_name="User password", max_length=128, default=None
    )
    avatar_url = models.CharField(
        max_length=550, verbose_name="avatar url", null=True, blank=True
    )
    street_address = models.CharField(
        max_length=100,
        verbose_name="User's street address",
        null=True,
        blank=True,
        default=None,
    )
    city = models.CharField(
        max_length=100, verbose_name="User's city", null=True, blank=True, default=None
    )
    state_of_residence = models.CharField(
        max_length=100,
        verbose_name="User's state of residence",
        null=True,
        blank=True,
        default=None,
    )
    country = models.CharField(
        max_length=100,
        verbose_name="User's Country",
        null=True,
        blank=True,
        default="Nigeria",
    )
    bio = models.TextField(verbose_name="User short bio", blank=True, default="")
    user_type = models.CharField(choices=USER_TYPE_CHOICES, verbose_name="User type")
    date_of_birth = models.DateField(
        verbose_name="Date of Birth", null=True, blank=True
    )
    last_login_user_type = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="User's last user_type login",
    )
    is_deactivated = models.BooleanField(
        "is user deactivated",
        default=False,
        help_text="Designates whether the user can login or not.",
    )
    deactivated_reason = models.TextField(
        null=True, blank=True, verbose_name="Why was this user deactivated?"
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        db_table = "user"
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.display_name

    @property
    def display_name(self):
        return (
            f"{self.first_name.title()} {self.last_name.title()}"
            if all([self.first_name, self.last_name])
            else f"{self.email or self.phone_number}"
        )

    @property
    def full_name(self):
        return (
            f"{self.first_name.title()} {self.last_name.title()}"
            if all([self.first_name, self.last_name])
            else ""
        )

    @property
    def user_location(self):
        return f"{self.street_address}, {self.city}, {self.state_of_residence}"

    def hard_delete(self, using=None, keep_parents=False, image_url=None, commit=True):
        """Hard deleting"""
        if self.avatar_url:
            return super(User, self).hard_delete(
                using=using, keep_parents=keep_parents, image_url=self.avatar_url
            )
        return super(User, self).hard_delete(using=using, keep_parents=keep_parents)


class UserActivity(BaseAbstractModel):
    """
    User Activity Model
    """

    category = models.CharField(max_length=100, verbose_name="User Activity Category")
    action = models.CharField(max_length=100, verbose_name="User Activity Action")
    context = models.JSONField(
        default=dict, verbose_name="User Activity Context", null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="user"
    )
    rider = models.ForeignKey(
        "rider.Rider", on_delete=models.CASCADE, null=True, verbose_name="rider"
    )
    customer = models.ForeignKey(
        "customer.Customer",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="customer",
    )

    ACTIVITY_LEVELS = [
        ("ERROR", "ERROR"),
        ("SUCCESS", "SUCCESS"),
        ("INFO", "INFO"),
        ("WARNING", "WARNING"),
    ]

    level = models.CharField(
        max_length=100,
        choices=ACTIVITY_LEVELS,
        default="INFO",
        verbose_name="User Activity Level",
    )
    session_id = models.CharField(
        max_length=60, null=True, blank=True, verbose_name="User Activity Session Id"
    )

    def __str__(self):
        return f"{self.user} - {self.action} ({self.category})"

    class Meta:
        db_table = "user_activity"
        verbose_name = "user activity"
        verbose_name_plural = "user activities"
