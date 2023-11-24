from django.utils import timezone

from order.models import Vehicle


class VehicleService:
    @classmethod
    def get_available_vehicles(cls):
        current_datetime = timezone.now()
        return Vehicle.objects.filter(
            status=Vehicle.STATUS[0][0],  # "ACTIVE"
            start_date__lte=current_datetime,
            end_date__gte=current_datetime,
        )
