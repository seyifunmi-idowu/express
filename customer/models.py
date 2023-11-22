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
    business_name = models.CharField(max_length=100, null=True, blank=True)
    business_address = models.CharField(max_length=100, null=True, blank=True)
    business_category = models.CharField(max_length=100, null=True, blank=True)
    delivery_volume = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.display_name

    @property
    def display_name(self):
        if self.customer_type == "INDIVIDUAL":
            return self.user.display_name
        return self.business_name if self.business_name else self.user.display_name

    class Meta:
        db_table = "customer"
        verbose_name = "customer"
        verbose_name_plural = "customers"


class IndividualCustomer(Customer):
    class Meta:
        proxy = True
        verbose_name = "Customer (Individual)"


class BusinessCustomer(Customer):
    class Meta:
        proxy = True
        verbose_name = "Customer (Business)"
