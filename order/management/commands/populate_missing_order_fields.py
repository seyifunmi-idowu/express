from django.core.management.base import BaseCommand
from django.db.models import Q

from order.models import Order
from order.service import MapService


class Command(BaseCommand):
    """
    This postfix is to populate missing fields in order table.
    """

    def get_orders_with_missing_fields(self):
        missing_fields_query = (
            Q(delivery_location_longitude__isnull=True)
            | Q(delivery_location_longitude="")
            | Q(delivery_location_latitude__isnull=True)
            | Q(delivery_location_latitude="")
            | Q(delivery_name__isnull=True)
            | Q(delivery_name="")
            | Q(delivery_location__isnull=True)
            | Q(delivery_location="")
            | Q(pickup_location__isnull=True)
            | Q(pickup_location="")
            | Q(pickup_name__isnull=True)
            | Q(pickup_name="")
            | Q(pickup_location_longitude__isnull=True)
            | Q(pickup_location_longitude="")
            | Q(pickup_location_latitude__isnull=True)
            | Q(pickup_location_latitude="")
        )

        return Order.objects.filter(missing_fields_query)

    def handle(self, *args, **kwargs):
        orders = self.get_orders_with_missing_fields()

        self.stdout.write(
            self.style.WARNING(
                f"Initializing Postfix to populate missing fields in order table for {orders.count()} orders..."
            )
        )
        order_affected = 0

        for order in orders:
            # Parse order_meta_data
            meta_data = order.order_meta_data
            timeline = meta_data.get("timeline", [])
            if not timeline:
                continue

            # Assume first timeline entry for simplicity
            first_timeline_entry = timeline[0]
            to_data = first_timeline_entry.get("to", {})
            from_data = first_timeline_entry.get("from", {})

            address_info2 = MapService.search_address(
                f"{from_data.get('latitude')},{from_data.get('longitude')}"
            )
            if not order.pickup_location_longitude:
                order.pickup_location_longitude = from_data.get("longitude")
            if not order.pickup_location_latitude:
                order.pickup_location_latitude = from_data.get("latitude")
            if not order.pickup_name:
                order.pickup_name = address_info2[0].get("name")
            if not order.pickup_location:
                order.pickup_location = address_info2[0].get("formatted_address")

            address_info = MapService.search_address(
                f"{to_data.get('latitude')},{to_data.get('longitude')}"
            )
            # Update order fields if they are missing
            if not order.delivery_location_longitude:
                order.delivery_location_longitude = to_data.get("longitude")
            if not order.delivery_location_latitude:
                order.delivery_location_latitude = to_data.get("latitude")
            if not order.delivery_name:
                order.delivery_name = to_data.get("name")
            if not order.delivery_name:
                order.delivery_name = address_info[0].get("name")
            if not order.delivery_location:
                order.delivery_location = address_info[0].get("formatted_address")

            self.stdout.write(self.style.SUCCESS(f"order id {order.id} "))
            # Save updated order
            order.save()
            order_affected += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Completed Postfix to populate missing fields in order table for {order_affected} orders."
            )
        )
