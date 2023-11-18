from decimal import Decimal

from rest_framework import status

from authentication.tasks import track_user_activity
from feleexpress import settings
from helpers.exceptions import CustomAPIException
from helpers.paystack_service import PaystackService
from wallet.models import BankAccount, Card, Transaction, Wallet


class WalletService:
    @classmethod
    def create_user_wallet(cls, user):
        return Wallet.objects.create(user=user)

    @classmethod
    def get_user_banks(cls, user):
        return BankAccount.objects.filter(user=user, save_account=True)

    @classmethod
    def get_bank_name_with_bank_code(cls, bank_code):
        banks = PaystackService.get_banks()
        bank_details = next((bank for bank in banks if bank_code == bank["code"]), {})
        return bank_details.get("name")

    @classmethod
    def get_or_create_transfer_recipient(
        cls, user, bank_code, account_number, save=False
    ):
        user_bank = BankAccount.objects.filter(
            user=user, account_number=account_number, bank_code=bank_code
        )
        if user_bank:
            return user_bank.first().recipient_code

        verify_account = PaystackService.verify_account_number(
            bank_code, account_number
        )
        if not verify_account["status"]:
            raise CustomAPIException(
                "Unable to verify account number", status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        account_name = verify_account["data"]["account_name"]
        response = PaystackService.create_transfer_recipient(
            account_name, bank_code, account_number
        )
        if not response["status"]:
            raise CustomAPIException(
                "Error occurred, unable to transfer",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        recipient_code = response["data"]["recipient_code"]
        bank_name = cls.get_bank_name_with_bank_code(bank_code)
        BankAccount.objects.create(
            user=user,
            account_number=account_number,
            account_name=account_name,
            bank_code=bank_code,
            bank_name=bank_name,
            recipient_code=recipient_code,
            meta=response,
            save_account=save,
        )
        return recipient_code

    @classmethod
    def withdraw_from_wallet(cls, user, amount, recipient_code, session_id):
        paystack_response = PaystackService.initiate_transfer(amount, recipient_code)
        user_wallet = user.get_user_wallet()
        user_wallet.withdraw(amount)
        reference = paystack_response["data"]["reference"]
        transaction_obj = TransactionService.create_transaction(
            transaction_type="DEBIT",
            transaction_status="SUCCESS",
            amount=Decimal(amount),
            user=user,
            reference=reference,
            pssp="PAYSTACK",
            payment_category="WITHDRAW",
            pssp_meta_data=paystack_response["data"],
        )
        activity_data = {
            "user": user.display_name,
            "transaction_id": transaction_obj.id,
        }
        track_user_activity(
            context=activity_data,
            category="USER_WALLET",
            action="USER_WITHDRAW",
            email=user.email,
            level="SUCCESS",
            session_id=session_id,
        )

    @classmethod
    def transfer_from_wallet_bank_account(cls, user, data, session_id):
        amount = float(data.get("amount"))
        account_number = data.get("account_number")
        bank_code = data.get("bank_code")
        save_account = data.get("save_account")

        user_wallet = user.get_user_wallet()
        if amount > user_wallet.balance:
            raise CustomAPIException(
                "Insufficient balance", status.HTTP_400_BAD_REQUEST
            )

        recipient_code = cls.get_or_create_transfer_recipient(
            user, bank_code, account_number, save_account
        )
        cls.withdraw_from_wallet(user, amount, recipient_code, session_id)
        return True

    @classmethod
    def transfer_from_wallet_to_beneficiary(
        cls, user, session_id, amount, beneficiary_id
    ):
        amount = float(amount)
        user_wallet = user.get_user_wallet()
        if amount > user_wallet.balance:
            raise CustomAPIException(
                "Insufficient balance", status.HTTP_400_BAD_REQUEST
            )

        bank_account = BankAccount.objects.get(id=beneficiary_id)
        if not bank_account:
            raise CustomAPIException("Beneficiary not found", status.HTTP_404_NOT_FOUND)
        cls.withdraw_from_wallet(user, amount, bank_account.recipient_code, session_id)
        return True


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
    def get_user_transaction(cls, user):
        return Transaction.objects.filter(user=user)


class CardService:
    @classmethod
    def get_user_cards(cls, user, **kwargs):
        return Card.objects.filter(user=user, **kwargs)

    @classmethod
    def create_user_card(cls, user, **kwargs):
        return Card.objects.create(user=user, **kwargs)

    @classmethod
    def initiate_card_transaction(cls, user, session_id, amount=100):
        base_url = settings.BASE_URL
        callback_url = f"{base_url}api/v1/paystack/paystack/callback"

        transaction = TransactionService.get_transaction(
            user=user,
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
        transaction_obj = TransactionService.create_transaction(
            transaction_type="CREDIT",
            transaction_status="PENDING",
            amount=Decimal(amount),
            user=user,
            reference=reference,
            pssp="PAYSTACK",
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
            category="USER_CARD",
            action="INITIATE_CARD_TRANSACTION",
            email=user.email,
            level="SUCCESS",
            session_id=session_id,
        )
        return {"url": authorization_url}

    @classmethod
    def verify_card_transaction(cls, data):
        reference = data.get("trxref", "")
        transaction = TransactionService.get_transaction_with_reference(
            reference
        ).first()
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
            user = transaction.user
            wallet = user.get_user_wallet()
            data = response["data"]
            amount = data["amount"] / 100

            transaction.transaction_status = "SUCCESS"
            transaction.wallet_id = wallet.id
            transaction.save()

            wallet.deposit(amount)

            card = Card.objects.filter(
                user=user,
                last_4=data["authorization"]["last4"],
                exp_month=data["authorization"]["exp_month"],
                exp_year=data["authorization"]["exp_year"],
            ).first()
            if not card:
                CardService.create_user_card(
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

    @classmethod
    def debit_card(cls, user, session_id, card_id, amount):

        user_card = cls.get_user_cards(user=user, id=card_id).first()
        if user_card is None:
            raise CustomAPIException("Card not found", status.HTTP_404_NOT_FOUND)
        response = PaystackService.charge_card(user.email, amount, user_card.card_auth)
        if response["status"] and response["data"]["status"] == "success":
            wallet = user.get_user_wallet()
            reference = response["data"]["reference"]
            TransactionService.create_transaction(
                transaction_type="CREDIT",
                transaction_status="SUCCESS",
                amount=Decimal(amount),
                user=user,
                reference=reference,
                pssp="PAYSTACK",
                payment_category="FUND_WALLET",
                wallet_id=wallet.id,
            )
            wallet.deposit(amount)

            activity_data = {
                "user": user.display_name,
                "card_id": card_id,
                "wallet_id": wallet.id,
            }
            track_user_activity(
                context=activity_data,
                category="USER_CARD",
                action="DEBIT_CARD_TRANSACTION",
                email=user.email,
                level="SUCCESS",
                session_id=session_id,
            )
            return True
        raise CustomAPIException("Unable to debit card", status.HTTP_400_BAD_REQUEST)
