from django.db import models

from feleexpress import settings
from helpers.db_helpers import BaseAbstractModel

# Create your models here.


class Rider(BaseAbstractModel):
    """
    Riders Model
    """

    STATUS = [
        ("APPROVED", "APPROVED"),
        ("UNAPPROVED", "UNAPPROVED"),
        ("SUSPENDED", "SUSPENDED"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="user",
        related_name="rider",
    )
    vehicle = models.ForeignKey(
        "order.Vehicle",
        on_delete=models.CASCADE,
        verbose_name="rider vehicle",
        blank=True,
        null=True,
    )
    vehicle_type = models.CharField(
        max_length=30, verbose_name="rider's vehicle type", blank=True, null=True
    )
    vehicle_make = models.CharField(max_length=50, blank=True, null=True)
    vehicle_model = models.CharField(max_length=30, blank=True, null=True)
    vehicle_plate_number = models.CharField(max_length=10, blank=True, null=True)
    vehicle_color = models.CharField(max_length=30, blank=True, null=True)
    rider_info = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    avatar_url = models.CharField(
        max_length=550, verbose_name="avatar url", null=True, blank=True
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS,
        default="UNAPPROVED",
        verbose_name="Rider workspace status",
    )
    status_updates = models.JSONField(default=list, null=True, blank=True)
    operation_locations = models.JSONField(
        default=list,
        null=True,
        blank=True,
        verbose_name="Locations where rider operate in Nigeria",
    )

    class Meta:
        db_table = "rider"
        verbose_name = "rider"
        verbose_name_plural = "rider"

    def __str__(self):
        return f"{self.display_name} - {self.status}"

    @property
    def display_name(self):
        return self.user.display_name

    @property
    def rating(self):
        from django.db.models import Avg

        rider_ratings = self.rider_rating.all()
        avg_rating = rider_ratings.aggregate(avg_rating=Avg("rating"))["avg_rating"]
        # Check if avg_rating is not None before returning
        return avg_rating if avg_rating is not None else 0.0

    def vehicle_photos(self):
        return self.rider_document.filter(type="vehicle_photo").values_list(
            "file_url", flat=True
        )

    def kyc_verified(self):
        # The document types you want to check
        document_types_to_check = [
            "vehicle_photo",
            "passport_photo",
            "government_id",
            "guarantor_letter",
            "address_verification",
        ]

        for document_type in document_types_to_check:
            rider_documents = self.rider_document.filter(type=document_type)
            if not rider_documents.exists():
                return False

            all_verified = all(document.verified for document in rider_documents)
            if not all_verified:
                return False

        return True

    def hard_delete(self, using=None, keep_parents=False, image_url=None, commit=True):
        """Hard deleting"""
        if self.avatar_url:
            return super(Rider, self).hard_delete(
                using=using, keep_parents=keep_parents, image_url=self.avatar_url
            )
        return super(Rider, self).hard_delete(using=using, keep_parents=keep_parents)


class ApprovedRider(Rider):
    class Meta:
        proxy = True
        verbose_name = "Rider (Approved)"


class UnApprovedRider(Rider):
    class Meta:
        proxy = True
        verbose_name = "Rider (Unapproved)"


class Guarantor(BaseAbstractModel):
    """
    Provider Guarantor Model
    """

    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=350, verbose_name="full name")
    address = models.CharField(max_length=550, verbose_name="address")
    email = models.CharField(max_length=100, verbose_name="Email")
    phone_number = models.CharField(max_length=20, verbose_name="phone number")
    relationship = models.CharField(
        max_length=100, verbose_name="relationship with the provider"
    )
    contact_mode = models.CharField(
        max_length=100, verbose_name="best mode to contact the reference"
    )
    guarantor_letter = models.CharField(max_length=550, verbose_name="address")
    verified = models.BooleanField(default=False, verbose_name="Is reference verified?")

    def __str__(self):
        return f"{self.rider.display_name}"

    class Meta:
        db_table = "guarantor"
        verbose_name = "guarantor"
        verbose_name_plural = "guarantor"


class RiderDocument(BaseAbstractModel):
    """
    Rider Document(s) Model
    """

    DOCUMENT_TYPES = [
        ("address_verification", "Address Verification (Utility Bill)"),
        ("driver_license", "Driver License"),
        ("insurance_certificate", "Insurance Certificate"),
        ("government_id", "Government Issued Identification"),
        ("guarantor_letter", "Guarantor Letter"),
        ("passport_photo", "Passport Photo"),
        ("vehicle_registration", "Vehicle Registration"),
        ("vehicle_photo", "Vehicle Photo"),
        ("certificate_of_vehicle_registration", "Certificate Of Vehicle Registration"),
        ("authorization_letter", "Authorization Letter"),
    ]
    type = models.CharField(
        max_length=100, choices=DOCUMENT_TYPES, verbose_name="document type"
    )
    number = models.CharField(
        max_length=50, verbose_name="document number", null=True, blank=True
    )
    file_url = models.CharField(
        max_length=550, verbose_name="document file url", null=True, blank=True
    )
    rider = models.ForeignKey(
        Rider,
        on_delete=models.CASCADE,
        verbose_name="rider",
        related_name="rider_document",
    )
    verified = models.BooleanField(default=False, verbose_name="Is Verified")

    def __str__(self):
        return f"{self.rider.display_name} - {self.type}"

    def hard_delete(self, using=None, keep_parents=False, image_url=None, commit=True):
        """Hard deleting"""
        if self.file_url:
            return super(RiderDocument, self).hard_delete(
                using=using, keep_parents=keep_parents, image_url=self.file_url
            )
        return super(RiderDocument, self).hard_delete(
            using=using, keep_parents=keep_parents
        )

    class Meta:
        db_table = "rider_document"
        verbose_name = "Rider Document"
        verbose_name_plural = "Rider Documents"


class RiderRating(BaseAbstractModel):
    RATING_CHOICES = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"))

    rating = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES)
    remark = models.TextField(blank=True, null=True)
    rider = models.ForeignKey(
        "rider.Rider",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="rider",
        related_name="rider_rating",
    )
    customer = models.ForeignKey(
        "customer.Customer",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="customer",
        related_name="customer_rating",
    )

    class Meta:
        db_table = "rider_rating"
        verbose_name = "Rider Rating"
        verbose_name_plural = "Rider Ratings"
