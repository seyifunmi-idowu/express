from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser

from feleexpress.middlewares.permissions.is_authenticated import (
    IsApprovedRider,
    IsAuthenticated,
    IsCustomer,
    IsRider,
)
from helpers.db_helpers import generate_session_id
from helpers.googlemaps_service import GoogleMapsService
from helpers.utils import ResponseManager, paginate_response
from order.docs import schema_doc
from order.serializers import (
    AddDriverTipSerializer,
    AssignRiderSerializer,
    CustomerCancelOrder,
    CustomerOrderSerializer,
    GetCurrentOrder,
    GetCustomerOrderSerializer,
    GetOrderSerializer,
    InitiateOrderSerializer,
    OrderHistorySerializer,
    PlaceOrderSerializer,
    RateRiderSerializer,
    RetrieveVehicleSerializer,
    RiderFailedPickupSerializer,
    RiderOrderSerializer,
    RiderPickUpOrderSerializer,
    SearchAddressSerializer,
)
from order.service import MapService, OrderService, VehicleService


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


class MapsViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, IsCustomer)

    # @swagger_auto_schema(
    #     methods=["post"],
    #     request_body=GetAddressInfoSerializer,
    #     operation_description="Get address information",
    #     operation_summary="Get address information",
    #     tags=["Maps"],
    #     responses=schema_doc.ADDRESS_INFO_RESPONSE,
    # )
    # @action(detail=False, methods=["post"], url_path="address-info")
    # def get_address_information(self, request):
    #     serialized_data = GetAddressInfoSerializer(data=request.data)
    #     if not serialized_data.is_valid():
    #         return ResponseManager.handle_response(
    #             errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
    #         )
    #     if serialized_data.data.get("address") is not None:
    #         response = MapService.get_info_from_address(
    #             serialized_data.data.get("address")
    #         )
    #     else:
    #         response = MapService.get_info_from_latitude_and_longitude(
    #             serialized_data.validated_data.get("latitude"),
    #             serialized_data.validated_data.get("longitude"),
    #         )
    #     return ResponseManager.handle_response(
    #         data=response, status=status.HTTP_200_OK, message="Address information"
    #     )

    @swagger_auto_schema(
        methods=["post"],
        request_body=SearchAddressSerializer,
        operation_description="Search address",
        operation_summary="This endpoint is use to search for address",
        tags=["Maps"],
        responses=schema_doc.ADDRESS_INFO_RESPONSE,
    )
    @action(detail=False, methods=["post"], url_path="address-info")
    def search_for_address(self, request):
        serialized_data = SearchAddressSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        response = MapService.search_address(serialized_data.data.get("address"))
        return ResponseManager.handle_response(
            data=response, status=status.HTTP_200_OK, message="Address information"
        )


class CustomerOrderViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, IsCustomer)

    @swagger_auto_schema(
        methods=["get"],
        operation_description="Get customer order history",
        operation_summary="Get customer order history",
        tags=["Customer-Order"],
        responses=schema_doc.GET_ORDER_HISTORY_RESPONSE,
    )
    @action(detail=False, methods=["get"], url_path="history")
    def get_history_order(self, request):
        orders = OrderService.get_order_qs(customer__user=request.user).order_by(
            "-created_at"
        )
        return paginate_response(
            queryset=orders, serializer_=OrderHistorySerializer, request=request
        )

    @swagger_auto_schema(
        operation_description="Get all ongoing orders",
        operation_summary="Get all ongoing orders",
        tags=["Customer-Order"],
        responses=schema_doc.GET_ALL_ORDER_RESPONSE,
    )
    @action(detail=False, methods=["get"], url_path="ongoing")
    def get_ongoing_orders(self, request):
        orders = OrderService.get_order_qs(customer__user=request.user).exclude(
            status__in=["ORDER_COMPLETED", "ORDER_CANCELLED"]
        )
        return paginate_response(
            queryset=orders, serializer_=GetCustomerOrderSerializer, request=request
        )

    @swagger_auto_schema(
        operation_description="Get all user orders",
        operation_summary="Get all user orders",
        tags=["Customer-Order"],
        responses=schema_doc.GET_ALL_ORDER_RESPONSE,
    )
    def list(self, request):
        orders = OrderService.get_order_qs(customer__user=request.user).order_by(
            "-created_at"
        )
        return paginate_response(
            queryset=orders, serializer_=GetCustomerOrderSerializer, request=request
        )

    @swagger_auto_schema(
        methods=["get"],
        operation_description="Get order information",
        operation_summary="Get order information",
        tags=["Customer-Order"],
        responses=schema_doc.GET_CUSTOMER_ORDER_RESPONSE,
    )
    @action(detail=False, methods=["get"], url_path="(?P<order_id>[a-z,A-Z,0-9]+)")
    def get_order(self, request, order_id):
        order = OrderService.get_order(order_id, customer__user=request.user)
        return ResponseManager.handle_response(
            data=CustomerOrderSerializer(order).data,
            status=status.HTTP_200_OK,
            message="Order Information",
        )

    @swagger_auto_schema(
        request_body=InitiateOrderSerializer,
        operation_description="Initiate order",
        operation_summary="Initiate order",
        tags=["Customer-Order"],
        responses=schema_doc.INITIATE_ORDER_RESPONSE,
    )
    @parser_classes([MultiPartParser, FormParser])
    def create(self, request):
        serialized_data = InitiateOrderSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        response = OrderService.initiate_order(
            request.user, serialized_data.validated_data
        )
        return ResponseManager.handle_response(
            data=response, status=status.HTTP_200_OK, message="Order Information"
        )

    @swagger_auto_schema(
        methods=["post"],
        request_body=PlaceOrderSerializer,
        operation_description="Place initiated order",
        operation_summary="Place initiated order",
        tags=["Customer-Order"],
        responses=schema_doc.PLACE_ORDER_RESPONSE,
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="(?P<order_id>[a-z,A-Z,0-9]+)/place-order",
    )
    def place_order(self, request, order_id):
        serialized_data = PlaceOrderSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        response = OrderService.place_order(
            request.user, order_id, serialized_data.data, generate_session_id()
        )
        return ResponseManager.handle_response(
            data=response, status=status.HTTP_200_OK, message="Finding nearby driver"
        )

    @swagger_auto_schema(
        methods=["post"],
        request_body=AddDriverTipSerializer,
        operation_description="Add Rider Tip",
        operation_summary="Add Rider Tip",
        tags=["Customer-Order"],
        responses=schema_doc.ADD_DRIVER_TIP_RESPONSE,
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="(?P<order_id>[a-z,A-Z,0-9]+)/add-rider-tip",
    )
    def add_rider_tip(self, request, order_id):
        serialized_data = AddDriverTipSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        response = OrderService.add_rider_tip(
            request.user,
            order_id,
            serialized_data.data.get("tip_amount"),
            generate_session_id(),
        )
        return ResponseManager.handle_response(
            data=response, status=status.HTTP_200_OK, message="Tip added"
        )

    @swagger_auto_schema(
        methods=["post"],
        request_body=AssignRiderSerializer,
        operation_description="Assign rider to pending order",
        operation_summary="Add rider to pending order",
        tags=["Customer-Order"],
        responses=schema_doc.ADD_DRIVER_TIP_RESPONSE,
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="(?P<order_id>[a-z,A-Z,0-9]+)/assign-rider",
    )
    def assign_rider(self, request, order_id):
        serialized_data = AssignRiderSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        response = OrderService.assign_rider_to_order(
            request.user,
            order_id,
            serialized_data.data.get("rider_id"),
            generate_session_id(),
        )
        return ResponseManager.handle_response(
            data=response, status=status.HTTP_200_OK, message="Pending rider acceptance"
        )

    @swagger_auto_schema(
        methods=["post"],
        request_body=RateRiderSerializer,
        operation_description="Rate rider",
        operation_summary="Rate rider",
        tags=["Customer-Order"],
        responses=schema_doc.RATE_RIDER_RESPONSE,
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="(?P<order_id>[a-z,A-Z,0-9]+)/rate-rider",
    )
    def rate_rider(self, request, order_id):
        serialized_data = RateRiderSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        response = OrderService.rate_rider(
            request.user, order_id, generate_session_id(), **serialized_data.data
        )
        return ResponseManager.handle_response(
            data=response, status=status.HTTP_200_OK, message="Rider rated"
        )

    @swagger_auto_schema(
        methods=["post"],
        request_body=CustomerCancelOrder,
        operation_description="Customer cancel order",
        operation_summary="Customer cancel order",
        tags=["Customer-Order"],
        responses=schema_doc.ACCEPT_CUSTOMER_ORDER_RESPONSE,
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="(?P<order_id>[a-z,A-Z,0-9]+)/cancel-order",
    )
    def customer_cancel_order(self, request, order_id):
        serialized_data = CustomerCancelOrder(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        OrderService.customer_cancel_order(
            request.user,
            order_id,
            generate_session_id(),
            serialized_data.validated_data.get("reason"),
        )
        return ResponseManager.handle_response(
            data={}, status=status.HTTP_200_OK, message="Order successfully cancelled"
        )


class RiderOrderViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, IsRider, IsApprovedRider)

    @swagger_auto_schema(
        operation_description="Get all user orders",
        operation_summary="Get all user orders",
        tags=["Rider-Order"],
        responses=schema_doc.GET_ALL_ORDER_RESPONSE,
    )
    def list(self, request):
        orders = OrderService.get_order_qs(rider__user=request.user)
        return ResponseManager.handle_response(
            data=GetOrderSerializer(orders, many=True).data,
            status=status.HTTP_200_OK,
            message="User orders",
        )

    @swagger_auto_schema(
        methods=["get"],
        operation_description="Get completed orders",
        operation_summary="Get completed orders",
        tags=["Rider-Order"],
        responses=schema_doc.GET_CURRENT_ORDER_RESPONSE,
        manual_parameters=[schema_doc.TIMEFRAME, schema_doc.CREATED_AT],
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="completed",
        permission_classes=(IsAuthenticated, IsRider),
    )
    def get_completed_order(self, request):
        orders = OrderService.get_completed_order(request=request)
        return ResponseManager.handle_response(
            data=GetCurrentOrder(orders, many=True).data,
            status=status.HTTP_200_OK,
            message="Order Information",
        )

    @swagger_auto_schema(
        methods=["get"],
        operation_description="Get current orders",
        operation_summary="Get current orders",
        tags=["Rider-Order"],
        responses=schema_doc.GET_CURRENT_ORDER_RESPONSE,
    )
    @action(detail=False, methods=["get"], url_path="current")
    def get_current_order(self, request):
        orders = OrderService.get_current_order_qs(request.user)
        return ResponseManager.handle_response(
            data=GetCurrentOrder(orders, many=True).data,
            status=status.HTTP_200_OK,
            message="Order Information",
        )

    @swagger_auto_schema(
        methods=["get"],
        operation_description="Get failed orders",
        operation_summary="Get failed orders",
        tags=["Rider-Order"],
        responses=schema_doc.GET_CURRENT_ORDER_RESPONSE,
    )
    @action(detail=False, methods=["get"], url_path="failed")
    def get_failed_order(self, request):
        orders = OrderService.get_failed_order(request.user)
        return ResponseManager.handle_response(
            data=GetCurrentOrder(orders, many=True).data,
            status=status.HTTP_200_OK,
            message="Order Information",
        )

    @swagger_auto_schema(
        methods=["get"],
        operation_description="Get new orders",
        operation_summary="Get new orders",
        tags=["Rider-Order"],
        responses=schema_doc.GET_ALL_ORDER_RESPONSE,
    )
    @action(detail=False, methods=["get"], url_path="new")
    def get_new_order(self, request):
        orders = OrderService.get_new_order(user=request.user)
        return ResponseManager.handle_response(
            data=GetOrderSerializer(orders, many=True).data,
            status=status.HTTP_200_OK,
            message="Order Information",
        )

    @swagger_auto_schema(
        methods=["get"],
        operation_description="Get order information",
        operation_summary="Get order information",
        tags=["Rider-Order"],
        responses=schema_doc.ACCEPT_CUSTOMER_ORDER_RESPONSE,
    )
    @action(detail=False, methods=["get"], url_path="(?P<order_id>[a-z,A-Z,0-9]+)")
    def get_order(self, request, order_id):
        order = OrderService.get_order(order_id, rider__user=request.user)
        return ResponseManager.handle_response(
            data=RiderOrderSerializer(order).data,
            status=status.HTTP_200_OK,
            message="Order Information",
        )

    @swagger_auto_schema(
        methods=["post"],
        operation_description="Accept Customer Order",
        operation_summary="Accept Customer Order",
        tags=["Rider-Order"],
        responses=schema_doc.ACCEPT_CUSTOMER_ORDER_RESPONSE,
    )
    @action(
        detail=False, methods=["post"], url_path="(?P<order_id>[a-z,A-Z,0-9]+)/accept"
    )
    def rider_accept_customer_order(self, request, order_id):
        order = OrderService.rider_accept_customer_order(
            request.user, order_id, generate_session_id()
        )
        return ResponseManager.handle_response(
            data=RiderOrderSerializer(order).data,
            status=status.HTTP_200_OK,
            message="Order Information",
        )

    @swagger_auto_schema(
        methods=["post"],
        operation_description="Rider arrived at pick up",
        operation_summary="Rider arrived at pick up",
        tags=["Rider-Order"],
        responses=schema_doc.RIDER_PICKUP_ORDER_RESPONSE,
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="(?P<order_id>[a-z,A-Z,0-9]+)/at-pick-up",
    )
    def rider_at_pickup(self, request, order_id):
        OrderService.rider_at_pickup(order_id, request.user, generate_session_id())
        return ResponseManager.handle_response(
            data={}, status=status.HTTP_200_OK, message="Order Updated"
        )

    @swagger_auto_schema(
        methods=["post"],
        request_body=RiderPickUpOrderSerializer,
        operation_description="Rider picked up order",
        operation_summary="Rider picked up order",
        tags=["Rider-Order"],
        responses=schema_doc.RIDER_PICKUP_ORDER_RESPONSE,
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="(?P<order_id>[a-z,A-Z,0-9]+)/pick-up-order",
    )
    def rider_pickup_order(self, request, order_id):
        serialized_data = RiderPickUpOrderSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        OrderService.rider_at_order_pickup(
            order_id,
            request.user,
            serialized_data.validated_data.get("proof"),
            generate_session_id(),
        )
        return ResponseManager.handle_response(
            data={}, status=status.HTTP_200_OK, message="Order Updated"
        )

    @swagger_auto_schema(
        methods=["post"],
        request_body=RiderFailedPickupSerializer,
        operation_description="Rider picked up order",
        operation_summary="Rider picked up order",
        tags=["Rider-Order"],
        responses=schema_doc.RIDER_PICKUP_ORDER_RESPONSE,
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="(?P<order_id>[a-z,A-Z,0-9]+)/failed-pick-up",
    )
    def rider_failed_pickup(self, request, order_id):
        serialized_data = RiderFailedPickupSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        OrderService.rider_failed_pickup(
            order_id,
            request.user,
            serialized_data.validated_data.get("reason"),
            generate_session_id(),
        )
        return ResponseManager.handle_response(
            data={}, status=status.HTTP_200_OK, message="Order Updated"
        )

    @swagger_auto_schema(
        methods=["post"],
        request_body=RiderPickUpOrderSerializer,
        operation_description="Rider arrived at destination",
        operation_summary="Rider arrived at destination",
        tags=["Rider-Order"],
        responses=schema_doc.RIDER_PICKUP_ORDER_RESPONSE,
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="(?P<order_id>[a-z,A-Z,0-9]+)/at-destination",
    )
    def rider_at_destination(self, request, order_id):
        OrderService.rider_at_destination(order_id, request.user, generate_session_id())
        return ResponseManager.handle_response(
            data={}, status=status.HTTP_200_OK, message="Order Updated"
        )

    @swagger_auto_schema(
        methods=["post"],
        request_body=RiderPickUpOrderSerializer,
        operation_description="Rider made delivery",
        operation_summary="Rider made delivery",
        tags=["Rider-Order"],
        responses=schema_doc.RIDER_PICKUP_ORDER_RESPONSE,
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="(?P<order_id>[a-z,A-Z,0-9]+)/made-delivery",
    )
    def rider_made_delivery(self, request, order_id):
        serialized_data = RiderPickUpOrderSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        OrderService.rider_made_delivery(
            order_id,
            request.user,
            serialized_data.validated_data.get("proof"),
            generate_session_id(),
        )
        return ResponseManager.handle_response(
            data={}, status=status.HTTP_200_OK, message="Order Updated"
        )

    @swagger_auto_schema(
        methods=["post"],
        operation_description="Rider received payment",
        operation_summary="Rider received payment",
        tags=["Rider-Order"],
        responses=schema_doc.RIDER_RECEIVE_PAYMENT_RESPONSE,
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="(?P<order_id>[a-z,A-Z,0-9]+)/received-payment",
    )
    def rider_received_payment(self, request, order_id):
        order = OrderService.rider_received_payment(
            order_id, request.user, generate_session_id()
        )
        return ResponseManager.handle_response(
            data=RiderOrderSerializer(order).data,
            status=status.HTTP_200_OK,
            message="Order Updated",
        )


def view_map(request):
    key = GoogleMapsService.secret_key
    context = {"key": key}
    return render(request, "google/map.html", context)
