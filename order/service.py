from django.utils import timezone
from rest_framework import status

from helpers.exceptions import CustomAPIException
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

    @classmethod
    def get_vehicle(cls, vehicle_id, raise_404=True):
        vehicle = Vehicle.objects.filter(id=vehicle_id).first()
        if not vehicle and raise_404:
            raise CustomAPIException("Vehicle not found.", status.HTTP_404_NOT_FOUND)
        return vehicle
