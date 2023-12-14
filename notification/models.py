from django.db import models

from helpers.db_helpers import BaseAbstractModel


class Subscription(BaseAbstractModel):
    TYPE = [("ACTIVE", "ACTIVE"), ("INACTIVE", "INACTIVE")]
    subscription_type = models.CharField(max_length=50, choices=TYPE, default="")
