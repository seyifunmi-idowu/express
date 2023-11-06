from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action

from feleexpress.middlewares.permissions.is_authenticated import (
    IsAuthenticated,
    IsRider,
)
from feleexpress.middlewares.permissions.is_paystack import IsPaystack
from helpers.db_helpers import generate_session_id
from helpers.utils import ResponseManager
from wallet.docs import schema_doc
from wallet.serializers import CardSerializer
from wallet.service import CardService, TransactionService


class WalletViewset(viewsets.ViewSet):
    pass


class CardViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, IsRider)

    @swagger_auto_schema(
        operation_description="Get all cards",
        operation_summary="Get all cards",
        tags=["Rider-KYC"],
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
        tags=["Rider-KYC"],
        responses=schema_doc.INITIATE_CARD_TRANSACTION_RESPONSE,
    )
    @action(detail=False, methods=["get"], url_path="initiate")
    def initiate_card_transaction(self, request):
        session_id = generate_session_id()
        response = TransactionService.initiate_card_transaction(
            request.user, session_id
        )
        return ResponseManager.handle_response(
            data=response,
            status=status.HTTP_200_OK,
            message="Card transaction initiated",
        )


class TransactionViewset(viewsets.ViewSet):
    permission_classes = ()

    @action(detail=False, methods=["get"], url_path="paystack/callback")
    def paystack_callback_view(self, request):
        response = TransactionService.verify_card_transaction(request.GET)
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
            TransactionService.verify_card_transaction(data)
        return ResponseManager.handle_response(
            data={}, status=status.HTTP_200_OK, message="Webhook successful"
        )
