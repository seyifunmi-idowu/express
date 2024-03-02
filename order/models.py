from django.db import models

from helpers.db_helpers import BaseAbstractModel


class Vehicle(BaseAbstractModel):
    STATUS = [("ACTIVE", "ACTIVE"), ("INACTIVE", "INACTIVE")]
    name = models.CharField(max_length=50, verbose_name="vehicle name")
    status = models.CharField(
        max_length=30, choices=STATUS, default="UNAPPROVED", verbose_name="status"
    )
    note = models.CharField(
        max_length=550, verbose_name="vehicle note", null=True, blank=True
    )
    start_date = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name="Active period start date"
    )
    end_date = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name="Active period end date"
    )
    file_url = models.CharField(
        max_length=550, verbose_name="Vehicle image url", null=True, blank=True
    )
    base_fare = models.IntegerField()
    km_5_below_fare = models.IntegerField(verbose_name="price per km 0-5")
    km_5_above_fare = models.IntegerField(verbose_name="price per km 5 above")
    price_per_minute = models.IntegerField(verbose_name="price per minute", default=80)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "vehicle"
        verbose_name = "Available Vehicle"
        verbose_name_plural = "Available Vehicles"


class Address(BaseAbstractModel):
    customer = models.ForeignKey(
        "customer.Customer",
        on_delete=models.CASCADE,
        verbose_name="customer",
        related_name="customer_address",
    )
    formatted_address = models.CharField(max_length=255)
    longitude = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    landmark = models.CharField(max_length=100, null=True, blank=True)
    direction = models.CharField(max_length=255, null=True, blank=True)
    label = models.CharField(max_length=255, null=True, blank=True)
    meta_data = models.JSONField(null=True, blank=True)
    save_address = models.BooleanField(default=False)

    class Meta:
        db_table = "address"
        verbose_name = "address"
        verbose_name_plural = "addresses"


class Order(BaseAbstractModel):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PROCESSING_ORDER", "Processing"),
        ("PENDING_RIDER_CONFIRMATION", "Awaiting rider confirmation"),
        ("RIDER_ACCEPTED_ORDER", "Rider accepted order"),
        ("RIDER_AT_PICK_UP", "Rider at pick up"),
        ("RIDER_PICKED_UP_ORDER", "Rider picked up order"),
        ("ORDER_ARRIVED", "Order arrived"),
        ("ORDER_DELIVERED", "Order delivered"),
        ("ORDER_COMPLETED", "Order completed"),
        ("ORDER_CANCELLED", "Order cancelled"),
    ]
    PAYMENT_METHOD_CHOICES = [("CASH", "Cash"), ("WALLET", "Wallet")]
    PAYMENT_BY_CHOICES = [("RECEIVER", "Receiver"), ("SENDER", "Sender")]

    customer = models.ForeignKey(
        "customer.Customer",
        on_delete=models.CASCADE,
        verbose_name="customer",
        related_name="customer_order",
    )
    rider = models.ForeignKey(
        "rider.Rider",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="rider",
        related_name="rider_order",
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="vehicle",
        related_name="vehicle_order",
    )
    order_id = models.CharField(max_length=20)
    chat_id = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="PENDING")
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True
    )
    payment_by = models.CharField(
        max_length=50, choices=PAYMENT_BY_CHOICES, null=True, blank=True
    )
    paid = models.BooleanField(default=False)
    pickup_number = models.CharField(max_length=50, null=True, blank=True)
    pickup_contact_name = models.CharField(max_length=100, null=True, blank=True)
    pickup_location = models.CharField(max_length=255, null=True, blank=True)
    pickup_location_longitude = models.CharField(max_length=255, null=True, blank=True)
    pickup_location_latitude = models.CharField(max_length=255, null=True, blank=True)
    delivery_number = models.CharField(max_length=50, null=True, blank=True)
    delivery_contact_name = models.CharField(max_length=100, null=True, blank=True)
    delivery_location = models.CharField(max_length=255, null=True, blank=True)
    delivery_location_longitude = models.CharField(
        max_length=255, null=True, blank=True
    )
    delivery_location_latitude = models.CharField(max_length=255, null=True, blank=True)
    delivery_time = models.DateTimeField(null=True, blank=True)
    order_stop_overs_meta_data = models.JSONField(
        default=list, help_text="Stop overs information"
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    fele_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    paid_fele = models.BooleanField(default=False)
    tip_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    order_timeline = models.JSONField(
        default=list, help_text="Ordered timeline tracking"
    )
    # ["note_to_driver", "timeline", "promo_code", ]
    order_meta_data = models.JSONField(
        default=dict, help_text="Other order information"
    )
    distance = models.CharField(max_length=20, help_text="represented in meters")
    duration = models.CharField(max_length=20, help_text="represented in seconds")

    def __str__(self):
        return f"{self.customer.display_name}  #{self.order_id}"

    class Meta:
        db_table = "order"
        verbose_name = "order"
        verbose_name_plural = "orders"

    def get_pick_up_time(self):
        return next(
            (
                x["date"]
                for x in self.order_timeline
                if x["status"] == "RIDER_PICKED_UP_ORDER"
            ),
            None,
        )

    def get_delivery_time(self):
        return next(
            (
                x["date"]
                for x in self.order_timeline
                if x["status"] == "ORDER_DELIVERED"
            ),
            None,
        )


class OrderTimeline(BaseAbstractModel):
    order = models.ForeignKey(
        "order.Order",
        on_delete=models.CASCADE,
        verbose_name="customer",
        related_name="customer_order",
    )
    status = models.CharField(max_length=100)
    proof_url = models.CharField(max_length=550, null=True, blank=True)
    reason = models.CharField(max_length=100, null=True, blank=True)
    meta_data = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return self.status

    class Meta:
        db_table = "order_timeline"
        verbose_name = "Order Timeline"
        verbose_name_plural = "Order Timelines"

    def get_created_at(self):
        date = self.meta_data.get("date", None)
        return date if date else self.created_at
