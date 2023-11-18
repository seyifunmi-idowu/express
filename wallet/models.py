from decimal import Decimal

from django.db import models

from feleexpress import settings
from helpers.db_helpers import BaseAbstractModel


class Wallet(BaseAbstractModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="user_wallet", on_delete=models.CASCADE
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def deposit(self, amount):
        """
        Deposit money into the wallet.
        """
        self.balance += Decimal(amount)
        self.save()

    def withdraw(self, amount):
        """
        Withdraw money from the wallet.
        """
        if self.balance >= amount:
            self.balance -= Decimal(amount)
            self.save()
        else:
            raise ValueError("Insufficient balance for withdrawal.")

    def __str__(self):
        return f"{self.user}'s Wallet"


class Transaction(BaseAbstractModel):
    TRANSACTION_TYPE_CHOICES = (("CREDIT", "CREDIT"), ("DEBIT", "DEBIT"))
    TRANSACTION_STATUS_CHOICES = (
        ("PENDING", "PENDING"),
        ("SUCCESS", "SUCCESS"),
        ("FAILED", "FAILED"),
        ("REVERSED", "REVERSED"),
        ("CANCELLED", "CANCELLED"),
    )
    PSSP_CHOICES = (("PAYSTACK", "PAYSTACK"), ("IN_HOUSE", "IN HOUSE TRANSACTION"))
    OBJECT_CLASS_CHOICES = (("CUSTOMER", "CUSTOMER"), ("RIDER", "RIDER"))
    PAYMENT_CATEGORIES = (
        ("FUND_WALLET", "Fund wallet"),
        ("CUSTOMER_PAY_RIDER", "Customer pays rider"),
        ("RIDER_PAY_CUSTOMER", "Rider pays customer"),
        ("WITHDRAW", "Withdrawal"),
    )
    CURRENCIES = [("NGN", "₦")]

    user = models.ForeignKey(
        "authentication.User",
        related_name="transaction_user",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    transaction_type = models.CharField(
        max_length=255,
        choices=TRANSACTION_TYPE_CHOICES,
        default=TRANSACTION_TYPE_CHOICES[0][0],
    )
    transaction_status = models.CharField(
        max_length=255,
        choices=TRANSACTION_STATUS_CHOICES,
        default=TRANSACTION_STATUS_CHOICES[0][0],
    )
    amount = models.DecimalField(decimal_places=2, max_digits=30)
    currency = models.CharField(
        max_length=30,
        choices=CURRENCIES,
        default=CURRENCIES[0][1],
        verbose_name="transaction currency",
    )
    reference = models.CharField(max_length=255, null=True, blank=True)
    pssp = models.CharField(
        max_length=255, choices=PSSP_CHOICES, default=PSSP_CHOICES[0][0]
    )
    payment_channel = models.CharField(max_length=255, null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    wallet_id = models.CharField(max_length=255, null=True, blank=True)
    object_id = models.CharField(max_length=255, null=True, blank=True)
    object_class = models.CharField(
        max_length=255, choices=OBJECT_CLASS_CHOICES, null=True, blank=True
    )

    payment_category = models.CharField(
        max_length=255, choices=PAYMENT_CATEGORIES, null=True, blank=True
    )
    pssp_meta_data = models.JSONField(default=dict, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        db_table = "transactions"
        verbose_name = "transaction"
        verbose_name_plural = "transaction"

    def __str__(self):
        return f"{self.user} - {self.currency} {self.amount}"


class Card(BaseAbstractModel):
    user = models.ForeignKey(
        "authentication.User",
        related_name="user_card",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    card_type = models.CharField(max_length=30, null=True, blank=True)
    card_auth = models.CharField(max_length=30, null=True, blank=True)
    last_4 = models.CharField(max_length=30, null=True, blank=True)
    exp_month = models.CharField(max_length=30, null=True, blank=True)
    exp_year = models.CharField(max_length=30, null=True, blank=True)
    country_code = models.CharField(max_length=30, null=True, blank=True)
    brand = models.CharField(max_length=30, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    reusable = models.BooleanField(default=True)
    customer_code = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        db_table = "card"
        verbose_name = "card"
        verbose_name_plural = "cards"


class BankAccount(BaseAbstractModel):
    user = models.ForeignKey(
        "authentication.User",
        related_name="user_bank_account",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    account_number = models.CharField(max_length=30, null=True, blank=True)
    account_name = models.CharField(max_length=100, null=True, blank=True)
    bank_code = models.CharField(max_length=30, null=True, blank=True)
    bank_name = models.CharField(max_length=30, null=True, blank=True)
    recipient_code = models.CharField(max_length=30, null=True, blank=True)
    meta = models.JSONField(default=dict, null=True, blank=True)
    save_account = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} -{self.bank_name} ({self.account_number})"

    class Meta:
        ordering = ["-created_at"]
        db_table = "bank_account"
        verbose_name = "bank_account"
        verbose_name_plural = "bank accounts"
