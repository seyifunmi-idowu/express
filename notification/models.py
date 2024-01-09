from django.db import models

from feleexpress import settings
from helpers.db_helpers import BaseAbstractModel


class UserNotification(BaseAbstractModel):
    STATUS = [("ACTIVE", "ACTIVE"), ("INACTIVE", "INACTIVE")]
    TYPE = [("SMS", "SMS"), ("PUSH", "PUSH")]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="user",
        related_name="user_notification",
    )
    one_signal_id = models.CharField(max_length=100, verbose_name="one_signal id")
    external_id = models.CharField(max_length=100, verbose_name="external id")
    subscription_id = models.CharField(max_length=100, verbose_name="subscription id")
    status = models.CharField(choices=STATUS, verbose_name="notification status")
    notification_type = models.CharField(
        choices=TYPE, verbose_name="notification type", default="PUSH"
    )
    meta_data = models.JSONField(
        default=dict, verbose_name="User notification context", null=True
    )

    def __str__(self):
        return f"{self.user} -- {self.one_signal_id or self.external_id}"

    def get_phone_number(self):
        return self.meta_data.get("phone_number", None)

    class Meta:
        db_table = "user_notification"
        verbose_name = "User Notifications"
        verbose_name_plural = "User Notifications"


# class Subscription(BaseAbstractModel):
#     TYPE = [("ACTIVE", "ACTIVE"), ("INACTIVE", "INACTIVE")]
#     subscription_type = models.CharField(max_length=50, choices=TYPE, default="")
