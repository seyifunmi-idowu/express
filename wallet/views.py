from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action

from feleexpress.middlewares.permissions.is_authenticated import (
    IsAuthenticated,
    IsRider,
)
from feleexpress.middlewares.permissions.is_paystack import IsPaystack
from helpers.db_helpers import generate_session_id
from helpers.paystack_service import PaystackService
from helpers.utils import ResponseManager
from wallet.docs import schema_doc
from wallet.serializers import CardSerializer, ChargeCardSerializer
from wallet.service import CardService


class WalletViewset(viewsets.ViewSet):
    pass


class CardViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, IsRider)

    @swagger_auto_schema(
        operation_description="Get all cards",
        operation_summary="Get all cards",
        tags=["User-Card"],
        responses=schema_doc.INITIATE_CARD_TRANSACTION_RESPONSE,
    )
    def list(self, request):
        user_cards = CardService.get_user_cards(request.user)
        return ResponseManager.handle_response(
            data=CardSerializer(user_cards, many=True).data,
            status=status.HTTP_200_OK,
            message="User cards",
        )

    @swagger_auto_schema(
        methods=["get"],
        operation_description="Initiate a card transaction",
        operation_summary="Initiate a card transaction",
        tags=["User-Card"],
        responses=schema_doc.INITIATE_CARD_TRANSACTION_RESPONSE,
    )
    @action(detail=False, methods=["get"], url_path="initiate")
    def initiate_card_transaction(self, request):
        session_id = generate_session_id()
        response = CardService.initiate_card_transaction(request.user, session_id)
        return ResponseManager.handle_response(
            data=response,
            status=status.HTTP_200_OK,
            message="Card transaction initiated",
        )

    @swagger_auto_schema(
        methods=["post"],
        request_body=ChargeCardSerializer,
        operation_description="Debit user card",
        operation_summary="Debit user card",
        tags=["User-Card"],
        responses=schema_doc.DEBIT_USER_CARD_RESPONSE,
    )
    @action(detail=False, methods=["post"], url_path="debit")
    def debit_card(self, request):
        serialized_data = ChargeCardSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        session_id = generate_session_id()
        CardService.debit_card(request.user, session_id, **serialized_data.data)
        return ResponseManager.handle_response(
            data={}, status=status.HTTP_200_OK, message="Card debited"
        )


class BankViewset(viewsets.ViewSet):
    permission_classes = ()

    @swagger_auto_schema(
        methods=["get"],
        request_body=ChargeCardSerializer,
        operation_description="Get List of banks",
        operation_summary="Get List of banks",
        tags=["User-Bank"],
        responses=schema_doc.DEBIT_USER_CARD_RESPONSE,
    )
    @action(detail=False, methods=["get"], url_path="list")
    def get_list_of_banks(self, request):
        response = PaystackService.get_banks()
        return ResponseManager.handle_response(
            data=response, status=status.HTTP_200_OK, message="List of banks"
        )


class PaystackViewset(viewsets.ViewSet):
    permission_classes = ()

    @action(detail=False, methods=["get"], url_path="paystack/callback")
    def paystack_callback_view(self, request):
        response = CardService.verify_card_transaction(request.GET)
        return ResponseManager.handle_response(
            data=response, status=status.HTTP_200_OK, message="Transaction successful"
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="paystack/webhook",
        permission_classes=(IsPaystack,),
    )
    def paystack_webhook_view(self, request):
        request_data = request.data
        event = request_data.get("event")
        if event == "charge.success":
            data = {"trxref": request_data.get("data", {}).get("reference")}
            CardService.verify_card_transaction(data)
        return ResponseManager.handle_response(
            data={}, status=status.HTTP_200_OK, message="Webhook successful"
        )