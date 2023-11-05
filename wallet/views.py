from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action

from feleexpress.middlewares.permissions.is_authenticated import (
    IsAuthenticated,
    IsRider,
)
from helpers.db_helpers import generate_session_id
from helpers.utils import ResponseManager
from wallet.docs import schema_doc
from wallet.service import TransactionService


class WalletViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, IsRider)

    @swagger_auto_schema(
        methods=["get"],
        operation_description="Initiate a card transaction",
        operation_summary="Initiate a card transaction",
        tags=["Rider-KYC"],
        responses=schema_doc.INITIATE_CARD_TRANSACTION_RESPONSE,
    )
    @action(detail=False, methods=["get"], url_path="card/initiate")
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
        response = TransactionService.verify_transaction(request.GET)
        return ResponseManager.handle_response(
            data=response, status=status.HTTP_200_OK, message="Transaction successful"
        )
