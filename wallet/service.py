from decimal import Decimal

from rest_framework import status

from authentication.tasks import track_user_activity
from feleexpress import settings
from helpers.exceptions import CustomAPIException
from helpers.paystack_service import PaystackService
from wallet.models import Card, Transaction, Wallet


class WalletService:
    @classmethod
    def create_user_wallet(cls, user):
        return Wallet.objects.create(user=user)


class TransactionService:
    @classmethod
    def create_transaction(cls, **kwargs):
        return Transaction.objects.create(**kwargs)

    @classmethod
    def get_transaction(cls, **kwargs):
        return Transaction.objects.filter(**kwargs)

    @classmethod
    def get_transaction_with_reference(cls, reference):
        return Transaction.objects.filter(reference=reference)

    @classmethod
    def initiate_card_transaction(
        cls, user, session_id, amount=100, object_class="CUSTOMER"
    ):
        base_url = settings.BASE_URL
        callback_url = f"{base_url}api/v1/transaction/paystack/callback"

        transaction = cls.get_transaction(
            payee=user,
            amount=Decimal(amount),
            transaction_type="CREDIT",
            transaction_status="PENDING",
            pssp="PAYSTACK",
        ).first()
        if transaction:
            authorization_url = transaction.pssp_meta_data["authorization_url"]
            return {"url": authorization_url}

        paystack_response = PaystackService.initialize_payment(
            user.email, amount, callback_url=callback_url
        )
        authorization_url = paystack_response["data"]["authorization_url"]
        reference = paystack_response["data"]["reference"]
        transaction_obj = cls.create_transaction(
            transaction_type="CREDIT",
            transaction_status="PENDING",
            amount=Decimal(amount),
            payee=user,
            reference=reference,
            pssp="PAYSTACK",
            object_class=object_class,
            payment_category="FUND_WALLET",
            pssp_meta_data=paystack_response["data"],
        )
        activity_data = {
            "user": user.display_name,
            "transaction_id": transaction_obj.id,
            "paystack_response": paystack_response["data"],
        }
        track_user_activity(
            context=activity_data,
            category="USER_TRANSACTION",
            action="INITIATE_CARD_TRANSACTION",
            email=user.email,
            level="SUCCESS",
            session_id=session_id,
        )
        return {"url": authorization_url}

    @classmethod
    def verify_transaction(cls, data):
        reference = data.get("trxref", "")
        transaction = cls.get_transaction_with_reference(reference).first()
        if not transaction:
            raise CustomAPIException(
                "Transaction not found.", status.HTTP_404_NOT_FOUND
            )
        if transaction.transaction_status == "SUCCESS":
            raise CustomAPIException(
                "Transaction already verified.", status.HTTP_400_BAD_REQUEST
            )
        response = PaystackService.verify_transaction(reference)
        if response and response["data"]["status"] == "success":
            user = transaction.payee
            wallet = user.get_user_wallet()
            data = response["data"]
            amount = data["amount"] / 100
            transaction.transaction_status = "SUCCESS"
            transaction.wallet_id = (wallet.id,)
            transaction.save()
            wallet.deposit(Decimal(amount))

            card = Card.objects.filter(
                user=user,
                last_4=data["authorization"]["last4"],
                exp_month=data["authorization"]["exp_month"],
                exp_year=data["authorization"]["exp_year"],
            ).first()
            if not card:
                Card.objects.create(
                    user=user,
                    card_type=data["authorization"]["card_type"],
                    card_auth=data["authorization"]["authorization_code"],
                    last_4=data["authorization"]["last4"],
                    exp_month=data["authorization"]["exp_month"],
                    exp_year=data["authorization"]["exp_year"],
                    country_code=data["authorization"]["country_code"],
                    brand=data["authorization"]["brand"],
                    reusable=data["authorization"]["reusable"],
                    first_name=data["customer"]["first_name"],
                    last_name=data["customer"]["last_name"],
                    customer_code=data["customer"]["customer_code"],
                )
        return True
