from django.core.management.base import BaseCommand

from order.models import Order, OrderTimeline


class Command(BaseCommand):
    """
    This postfix is to migrate order_time from Order table to OrderTimeline table.
    """

    def handle(self, *args, **kwargs):
        order_qs = Order.objects.filter(order_timeline__isnull=False)

        self.stdout.write(
            self.style.WARNING(
                f"Initializing Postfix to migrate order_time from Order table to OrderTimeline table for {order_qs.count()} orders..."
            )
        )
        order_affected = 0
        for order in order_qs:
            order_timeline = order.order_timeline
            for timeline in order_timeline:
                proof_url = None
                status = timeline.pop("status")
                if status == "RIDER_PICKED_UP_ORDER":
                    proof_url = timeline.pop("proof_of_pickup_url")
                elif status == "ORDER_DELIVERED":
                    if timeline.get("proof_of_delivery_url"):
                        proof_url = timeline.pop("proof_of_delivery_url")

                reason = timeline.pop("reason", None)
                meta_data = timeline
                OrderTimeline.objects.create(
                    order=order,
                    status=status,
                    proof_url=proof_url,
                    reason=reason,
                    meta_data=meta_data,
                )
            order_affected += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Completed Postfix to migrate order_time from Order table to OrderTimeline table for {order_affected} orders."
            )
        )
