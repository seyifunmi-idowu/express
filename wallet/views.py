from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action

from feleexpress.middlewares.permissions.is_authenticated import (
    IsAuthenticated,
    IsCustomer,
    IsRider,
)
from feleexpress.middlewares.permissions.is_paystack import IsPaystack
from helpers.db_helpers import generate_session_id
from helpers.exceptions import CustomAPIException
from helpers.paystack_service import PaystackService
from helpers.utils import ResponseManager, paginate_response
from wallet.docs import schema_doc, schema_example
from wallet.serializers import (
    AddCardSerializer,
    BankAccountSerializer,
    CardSerializer,
    ChargeCardSerializer,
    GetTransactionsSerializer,
    TrasferFromWalletToBankSerializer,
    TrasferFromWalletToBeneficiarySerializer,
    VerifyAccountNumberSerializer,
)
from wallet.service import CardService, WalletService


class WalletViewset(viewsets.ViewSet):
    @swagger_auto_schema(
        methods=["post"],
        request_body=TrasferFromWalletToBankSerializer,
        operation_description="Transfer from wallet to bank account",
        operation_summary="Transfer from wallet to bank account",
        tags=["Wallet"],
        responses=schema_doc.TRANSFER_FROM_WALLET_BANK_RESPONSE,
    )
    @action(detail=False, methods=["post"], url_path="transfer/bank")
    def transfer_from_wallet_to_bank_account(self, request):
        serialized_data = TrasferFromWalletToBankSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        session_id = generate_session_id()
        response = WalletService.transfer_from_wallet_bank_account(
            request.user, serialized_data.validated_data, session_id
        )
        return ResponseManager.handle_response(
            data=response, status=status.HTTP_200_OK, message="Transfer in progress"
        )

    @swagger_auto_schema(
        methods=["post"],
        request_body=TrasferFromWalletToBeneficiarySerializer,
        operation_description="Transfer from wallet to beneficiary",
        operation_summary="Transfer from wallet to beneficiary",
        tags=["Wallet"],
        responses=schema_doc.TRANSFER_FROM_WALLET_BENEFICIARY_RESPONSE,
    )
    @action(detail=False, methods=["post"], url_path="transfer/beneficiary")
    def transfer_from_wallet_to_beneficiary(self, request):
        serialized_data = TrasferFromWalletToBeneficiarySerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        session_id = generate_session_id()
        response = WalletService.transfer_from_wallet_to_beneficiary(
            request.user, session_id, **serialized_data.validated_data
        )
        return ResponseManager.handle_response(
            data=response, status=status.HTTP_200_OK, message="Transfer in progress"
        )

    @swagger_auto_schema(
        methods=["get"],
        operation_description="Get user wallet transactions",
        operation_summary="Get user wallet transactions",
        tags=["Wallet"],
        manual_parameters=[
            schema_example.START_DATE_FILTERS,
            schema_example.END_DATE_FILTERS,
            schema_example.TRANSACTION_TYPE,
            schema_example.TRANSACTION_STATUS,
        ],
        responses=schema_doc.GET_USER_TRANSACTIONS_RESPONSE,
    )
    @action(detail=False, methods=["get"], url_path="transaction")
    def get_user_transactions(self, request):
        user_transactions = WalletService.get_user_wallet_transactions(request)
        return paginate_response(
            queryset=user_transactions,
            serializer_=GetTransactionsSerializer,
            request=request,
        )

    @swagger_auto_schema(
        methods=["get"],
        operation_description="Get user wallet balance",
        operation_summary="Get user wallet balance",
        tags=["Wallet"],
        responses=schema_doc.GET_USER_WALLET_BALANCE_RESPONSE,
    )
    @action(detail=False, methods=["get"], url_path="balance")
    def get_user_wallet_balance(self, request):
        user_wallet = request.user.get_user_wallet()
        return ResponseManager.handle_response(
            data={"balance": user_wallet.balance},
            status=status.HTTP_200_OK,
            message="Wallet balance",
        )


class CardViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, IsRider | IsCustomer)

    @swagger_auto_schema(
        operation_description="Get all cards",
        operation_summary="Get all cards",
        tags=["User-Card"],
        responses=schema_doc.GET_USER_CARD_RESPONSE,
    )
    def list(self, request):
        user_cards = CardService.get_user_cards(request.user)
        return ResponseManager.handle_response(
            data=CardSerializer(user_cards, many=True).data,
            status=status.HTTP_200_OK,
            message="User cards",
        )

    @swagger_auto_schema(
        methods=["post"],
        request_body=AddCardSerializer,
        operation_description="Initiate add card transaction",
        operation_summary="Initiate add card transaction",
        tags=["User-Card"],
        responses=schema_doc.INITIATE_CARD_TRANSACTION_RESPONSE,
    )
    @action(detail=False, methods=["post"], url_path="initiate")
    def initiate_card_transaction(self, request):
        serialized_data = AddCardSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        session_id = generate_session_id()
        response = CardService.initiate_card_transaction(
            request.user, session_id, serialized_data.data.get("amount")
        )
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
    permission_classes = (IsAuthenticated, IsRider)

    @swagger_auto_schema(
        methods=["get"],
        operation_description="Get List of banks",
        operation_summary="Get List of banks",
        tags=["User-Bank"],
        responses=schema_doc.GET_LIST_OF_BANKS_RESPONSE,
    )
    @action(detail=False, methods=["get"], url_path="list")
    def get_list_of_banks(self, request):
        response = PaystackService.get_banks()
        return ResponseManager.handle_response(
            data=response, status=status.HTTP_200_OK, message="List of banks"
        )

    @swagger_auto_schema(
        methods=["post"],
        request_body=VerifyAccountNumberSerializer,
        operation_description="Verify account number",
        operation_summary="Verify account number",
        tags=["User-Bank"],
        responses=schema_doc.VERIFY_ACCOUNT_NUMBER_RESPONSE,
    )
    @action(detail=False, methods=["post"], url_path="account-number")
    def verify_account_number(self, request):
        serialized_data = VerifyAccountNumberSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        response = PaystackService.verify_account_number(
            **serialized_data.validated_data
        )
        if not response["status"]:
            raise CustomAPIException(
                "Unable to verify account number", status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        return ResponseManager.handle_response(
            data={"account_name": response["data"]["account_name"]},
            status=status.HTTP_200_OK,
            message="Account name",
        )

    @swagger_auto_schema(
        methods=["get"],
        operation_description="Get beneficiary list",
        operation_summary="Get beneficiary accounts",
        tags=["User-Bank"],
        responses=schema_doc.GET_USER_BANKS_RESPONSE,
    )
    @action(detail=False, methods=["get"], url_path="user-beneficiary")
    def get_user_beneficiary(self, request):
        response = WalletService.get_user_banks(request.user)
        return ResponseManager.handle_response(
            data=BankAccountSerializer(response, many=True).data,
            status=status.HTTP_200_OK,
            message="User banks",
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
