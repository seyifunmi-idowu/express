from django.db import models

from feleexpress import settings
from helpers.db_helpers import BaseAbstractModel


class Notification(BaseAbstractModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="user",
        related_name="notification",
    )
    title = models.CharField(max_length=50, blank=True, null=True)
    message = models.CharField(max_length=500, blank=True, null=True)
    opened = models.BooleanField(default=False)
    meta_data = models.JSONField(default=dict, null=True)

    def __str__(self):
        return f"{self.user} -- {self.title}"

    class Meta:
        db_table = "notification"
        verbose_name = "Notifications"
        verbose_name_plural = "Notifications"


class UserNotification(BaseAbstractModel):
    STATUS = [("ACTIVE", "ACTIVE"), ("INACTIVE", "INACTIVE")]
    TYPE = [("SMS", "SMS"), ("PUSH", "PUSH")]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="user",
        related_name="user_notification",
    )
    one_signal_id = models.CharField(
        max_length=100, verbose_name="one_signal id", blank=True, null=True
    )
    external_id = models.CharField(
        max_length=100, verbose_name="external id", blank=True, null=True
    )
    subscription_id = models.CharField(
        max_length=100, verbose_name="subscription id", blank=True, null=True
    )
    status = models.CharField(
        choices=STATUS, verbose_name="notification status", default="ACTIVE"
    )
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


#
#
# class ThirdPartyNotification(BaseAbstractModel):
#     STATUS = [("ACTIVE", "ACTIVE"), ("INACTIVE", "INACTIVE")]
#     TYPE = [("SMS", "SMS"), ("PUSH", "PUSH")]
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     one_signal_id = models.CharField(max_length=100, blank=True, null=True)
#     external_id = models.CharField(max_length=100, blank=True, null=True)
#     subscription_id = models.CharField(max_length=100, blank=True, null=True)
#     status = models.CharField(choices=STATUS, default="ACTIVE")
#     notification_type = models.CharField(choices=TYPE, default="PUSH")
#     meta_data = models.JSONField(default=dict, null=True)
#
#     class Meta:
#         db_table = "third_party_notification"
#         verbose_name = "Third Party Notifications"
#         verbose_name_plural = "Third Party Notifications"
#
#     def __str__(self):
#         return f"{self.user} -- {self.one_signal_id or self.external_id}"
#
#     def get_phone_number(self):
#         return self.meta_data.get("phone_number", None)
