from decimal import Decimal

from authentication.tasks import track_user_activity
from helpers.paystack_service import PaystackService
from wallet.models import Transaction, Wallet


class WalletService:
    @classmethod
    def create_user_wallet(cls, user):
        return Wallet.objects.create(user=user)


class TransactionService:
    @classmethod
    def create_transaction(cls, **kwargs):
        return Transaction.objects.create(**kwargs)

    @classmethod
    def initiate_card_transaction(
        cls, user, session_id, amount=100, object_class="CUSTOMER"
    ):
        paystack_response = PaystackService.initialize_payment(user.email, amount)
        authorization_url = paystack_response["data"]["authorization_url"]
        reference = paystack_response["data"]["reference"]
        wallet = user.get_user_wallet()
        transaction_obj = cls.create_transaction(
            transaction_type="CREDIT",
            transaction_status="PENDING",
            amount=Decimal(amount),
            payee=user,
            reference=reference,
            pssp="PAYSTACK",
            object_class=object_class,
            wallet_id=wallet.id,
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
