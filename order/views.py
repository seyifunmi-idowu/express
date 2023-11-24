from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action

# from helpers.db_helpers import generate_session_id
from helpers.utils import ResponseManager
from order.docs import schema_doc
from order.serializers import RetrieveVehicleSerializer
from order.service import VehicleService


class VehicleViewset(viewsets.ViewSet):
    permission_classes = ()

    @swagger_auto_schema(
        methods=["get"],
        operation_description="Get available vehicles",
        operation_summary="Get available vehicles",
        tags=["Vehicle"],
        responses=schema_doc.RIDER_INFO_RESPONSE,
    )
    @action(detail=False, methods=["get"], url_path="available")
    def get_available_vehicles(self, request):
        vehicles = VehicleService.get_available_vehicles()
        return ResponseManager.handle_response(
            data=RetrieveVehicleSerializer(vehicles, many=True).data,
            status=status.HTTP_200_OK,
            message="Available vehicles",
        )
