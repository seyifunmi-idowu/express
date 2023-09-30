from django.db import models

from feleexpress import settings
from helpers.db_helpers import BaseAbstractModel


class Customer(BaseAbstractModel):
    """
    Customer Model
    """

    CUSTOMER_TYPE_CHOICES = [("INDIVIDUAL", "INDIVIDUAL"), ("BUSINESS", "BUSINESS")]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="user",
        related_name="customer",
    )
    customer_type = models.CharField(
        max_length=30, choices=CUSTOMER_TYPE_CHOICES, verbose_name="customer type"
    )
