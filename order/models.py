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
    # 0.1 - 5 km
    km_5_below_fare = models.IntegerField(verbose_name="0-5 km fare")
    # 5.1 and above
    km_5_above_fare = models.IntegerField(verbose_name="5km and above fare")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "vehicle"
        verbose_name = "Available Vehicle"
        verbose_name_plural = "Available Vehicles"


# class Order(BaseAbstractModel):
#     STATUS_CHOICES = [
#         ('PENDING', 'Pending'),
#         ('RIDER_ACCEPTED_ORDER', 'Rider accepted order'),
#         ('RIDER_PICKED_UP_ORDER', 'Rider picked up order'),
#         ('RIDER_PICKED_UP_ORDER', 'Rider picked up order'),
#         ('ORDER_ARRIVED', 'Order arrived'),
#         ('PROCESSING_ORDER', 'Processing'),
#         ('ORDER_DELIVERED', 'Order delivered'),
#         ('ORDER_CANCELLED', 'Order cancelled'),
#     ]
#
#     customer = models.ForeignKey(
#         "customer.Customer",
#         on_delete=models.CASCADE,
#         verbose_name="customer",
#         related_name="customer_order",
#     )
#     rider = models.ForeignKey(
#         "rider.Rider",
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         verbose_name="rider",
#         related_name="rider_order",
#     )
#     order_id = models.CharField(max_length=20)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
#     pickup_location = models.CharField(max_length=255, help_text='Pickup location address')
#     pickup_location_longitude = models.CharField(max_length=255, help_text='Pickup location longitude')
#     pickup_location_latitude = models.CharField(max_length=255, help_text='Pickup location latitude')
#     delivery_location = models.CharField(max_length=255, help_text='Delivery location address')
#     delivery_location_longitude = models.CharField(max_length=255, help_text='Delivery location longitude')
#     delivery_location_latitude = models.CharField(max_length=255, help_text='Delivery location latitude')
#     delivery_time = models.DateTimeField(null=True, blank=True, help_text='Scheduled delivery time')
#     order_location_meta_data = models.JSONField(help_text='JSON representation of locations information')
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
#     order_timeline = models.JSONField(help_text='JSON representation of ordered timeline tracking')
#     order_meta_data = models.JSONField(help_text='JSON representation of other order information')
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Order #{self.order_id} - {self.customer.display_name}"
#
#     class Meta:
#         db_table = "order"
#         verbose_name = "order"
#         verbose_name_plural = "orders"
