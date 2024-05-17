from django.db import models

from feleexpress import settings
from helpers.db_helpers import BaseAbstractModel


class Business(BaseAbstractModel):
    """
    Business Model
    """

    BUSINESS_TYPE_CHOICES = [("RESTAURANT", "Restaurant")]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="user",
        related_name="business",
    )
    business_type = models.CharField(
        max_length=30, choices=BUSINESS_TYPE_CHOICES, null=True, blank=True
    )
    business_name = models.CharField(max_length=100, null=True, blank=True)
    business_address = models.CharField(max_length=100, null=True, blank=True)
    business_category = models.CharField(max_length=100, null=True, blank=True)
    delivery_volume = models.IntegerField(null=True, blank=True)
    webhook_url = models.URLField(null=True, blank=True)
    e_secret_key = models.CharField(max_length=700, null=True, blank=True)

    def __str__(self):
        return self.business_name

    @property
    def display_name(self):
        return self.business_name if self.business_name else self.user.display_name

    class Meta:
        db_table = "business"
        verbose_name = "business"
        verbose_name_plural = "businesses"
