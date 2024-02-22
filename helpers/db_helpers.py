import random
import string
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.db import OperationalError, models, transaction
from django.db.models.query import QuerySet
from django.http import Http404
from django.utils import timezone
from rest_framework import status

from helpers.exceptions import CustomAPIException
from helpers.s3_uploader import S3Uploader


class BaseQuerySet(QuerySet):
    def delete(self):
        return super(BaseQuerySet, self).update(deleted_at=timezone.now())

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class BaseManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        super(BaseManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return BaseQuerySet(self.model).filter(deleted_at=None)
        return BaseQuerySet(self.model)


def generate_id():
    return uuid.uuid4().hex


def generate_session_id():
    return f"SESSION-{generate_id()}"


def generate_otp():
    return "".join(random.choices(string.digits, k=6))


def generate_referral_code(length=8):
    from authentication.models import User

    characters = string.ascii_letters + string.digits
    referral_code = "".join(random.choice(characters) for _ in range(length))
    if User.objects.filter(referral_code=referral_code).exists():
        return generate_referral_code(length=8)  #
    return referral_code


def generate_orderid():
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=10))


class BaseAbstractModel(models.Model):
    """Base Abstract Model"""

    RECORD_STATE = [("ACTIVE", "ACTIVE"), ("DELETED", "DELETED")]

    id = models.CharField(
        max_length=60, primary_key=True, default=generate_id, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    state = models.CharField(max_length=20, choices=RECORD_STATE, default="ACTIVE")
    created_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        verbose_name="created by",
        related_name="+",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        verbose_name="updated by",
        related_name="+",
        null=True,
        blank=True,
    )
    deleted_by = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        verbose_name="deleted by",
        related_name="+",
        null=True,
        blank=True,
    )

    objects = BaseManager()
    all_objects = BaseManager(alive_only=False)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def delete(self, soft_delete: bool = True, actor=None):
        if soft_delete:
            self.deleted_at = timezone.now()
            self.state = self.RECORD_STATE[1][0]
            self.deleted_by = actor
            return self.save()

    def hard_delete(self, using=None, keep_parents=False, image_url=None, commit=True):
        """Hard deleting"""
        if image_url:
            S3Uploader().hard_delete_object(image_url)
        if commit:
            return super(BaseAbstractModel, self).delete(
                using=using, keep_parents=keep_parents
            )

    def save(self, actor=None, *args, **kwargs):
        actor = kwargs.pop("actor", None)

        if actor:
            if not self.created_by:
                self.created_by = actor
            self.updated_by = actor
        super(BaseAbstractModel, self).save(*args, **kwargs)

    def undelete(self):
        self.deleted_at = None
        self.deleted_by = None
        self.state = self.RECORD_STATE[0][0]
        self.save()

    def update_self(self, data):
        for key, value in data.items():
            setattr(self, key, value)
            self.save()
        return self


def get_object_or_404(model, **kwargs):
    instance = model.objects.filter(**kwargs).first()
    if instance:
        return instance
    raise Http404


def select_for_update(model, **kwargs):
    """
    This retrieves a model instance and locks down that instance until the
    transaction is complete. This method should only be
    called in an atomic block.
    """
    instance = None
    try:
        instance = model.objects.select_for_update().get(**kwargs)
    except ObjectDoesNotExist:
        # Handle object not found
        raise Http404
    except OperationalError:
        # Handle database error
        raise CustomAPIException(
            "An operational error occurred", status.HTTP_400_BAD_REQUEST
        )
    except transaction.TransactionManagementError:
        # Handle transaction error
        raise CustomAPIException(
            "A transaction management error occurred", status.HTTP_400_BAD_REQUEST
        )
    return instance
