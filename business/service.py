import base64
from datetime import date
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.db import transaction
from django.utils import timezone

from authentication.service import AuthService, UserService
from authentication.tasks import track_user_activity
from business.models import Business
from helpers.encryption import EncryptionClass
from helpers.exceptions import CustomAPIException, CustomFieldValidationException
from helpers.paystack_service import PaystackService
from helpers.token_manager import TokenManager


class BusinessAuth:
    @classmethod
    def register_business_user(cls, data, session_id):
        data = data.copy()
        email = data.get("email")
        phone_number = data.get("phone_number")
        business_name = data.get("business_name")
        password = data.pop("password")

        with transaction.atomic():
            instance_user = UserService.create_user(
                email=email,
                first_name=business_name,
                phone_number=phone_number,
                user_type="BUSINESS",
                password=password,
                referral_code=None,
            )
            BusinessService.create_business(
                user=instance_user, business_name=business_name
            )

            AuthService.initiate_email_verification(email=email, name=business_name)

            track_user_activity(
                context=data,
                category="BUSINESS_AUTH",
                action="BUSINESS_SIGNUP",
                email=email,
                level="SUCCESS",
                session_id=session_id,
            )
        return {}

    @classmethod
    def login_business_user(cls, request, data, session_id):
        email = data.get("email")
        password = data.get("password")

        user = UserService.get_user_instance(email=email)

        if user is None:
            messages.add_message(
                request, messages.ERROR, "email or password is not correct"
            )
            return False

        if user.user_type != "BUSINESS":
            messages.add_message(
                request, messages.ERROR, "email or password is not correct"
            )
            return False

        is_valid_password = check_password(password, user.password)
        if not is_valid_password:
            messages.add_message(
                request, messages.ERROR, "email or password is not correct"
            )
            return False

        login(request, user)
        user.last_login = timezone.now()
        user.save()
        track_user_activity(
            context={},
            category="BUSINESS_AUTH",
            action="BUSINESS_USER_LOGIN_ATTEMPT_SUCCESS",
            email=user.email,
            level="SUCCESS",
            session_id=session_id,
        )
        return True

    @classmethod
    def verify_business_user_email(cls, request, data, session_id):
        user = UserService.get_user_instance(email=data.get("email"))
        if user is None:
            messages.add_message(request, messages.ERROR, "User not found.")
        else:
            try:
                AuthService.validate_email_verification(
                    email=data.get("email"),
                    code=data.get("code"),
                    session_id=session_id,
                )
                login(request, user)
                user.last_login = timezone.now()
                user.save()

            except CustomAPIException as e:
                messages.add_message(request, messages.ERROR, e.detail["message"])

            except CustomFieldValidationException as e:
                messages.add_message(
                    request, messages.ERROR, e.detail["errors"]["code"][0]
                )

    #  TODO: From this part below should not be in this class. Move it to BusinessService and test very well.
    @classmethod
    def get_business_dashboard_view(cls, user):
        from order.service import OrderService
        from wallet.service import TransactionService

        today = date.today()
        orders = OrderService.get_order_qs(business__user=user).order_by("-created_at")[
            :10
        ]
        total_orders = OrderService.get_order_qs(business__user=user).count()
        today_orders = (
            OrderService.get_order_qs(business__user=user)
            .filter(created_at__date=today)
            .count()
        )
        wallet_balance = user.get_user_wallet().balance
        transactions = TransactionService.get_user_transaction(user).order_by(
            "-created_at"
        )[:10]

        data = {
            "orders": orders,
            "total_orders": total_orders,
            "today_orders": today_orders,
            "wallet_balance": wallet_balance,
            "transactions": transactions,
        }
        return data

    @classmethod
    def get_business_order_view(cls, user):
        from order.service import OrderService

        orders = OrderService.get_order_qs(business__user=user).order_by("-created_at")
        return {"orders": orders}

    @classmethod
    def get_business_retrieve_order_view(cls, user, order_id):
        from order.service import OrderService

        order = OrderService.get_order_qs(id=order_id, business__user=user).first()
        if order is None:
            pass

        distance = OrderService.get_km_in_word(order.distance)
        duration = OrderService.get_time_in_word(order.duration)
        order_timeline = OrderService.get_order_timeline(order)
        return {
            "order": order,
            "distance": distance,
            "duration": duration,
            "order_timeline": order_timeline,
        }

    @classmethod
    def get_business_wallet_view(cls, user):
        from wallet.service import CardService, TransactionService, WalletService

        bank_accounts = WalletService.get_user_banks(user)
        cards = CardService.get_user_cards(user)
        transactions = TransactionService.get_user_transaction(user)
        data = {
            "bank_accounts": bank_accounts,
            "cards": cards,
            "transactions": transactions,
            "wallet_balance": user.get_user_wallet().balance,
        }
        return data

    @classmethod
    def regenerate_secret_key(cls, user, session_id):
        access_token = BusinessService.get_business_user_secret_key(user=user)
        if access_token is not None:
            TokenManager.logout(access_token)

        cls.generate_business_secret_key(user, session_id)
        track_user_activity(
            context={},
            category="BUSINESS_AUTH",
            action="BUSINESS_USER_REGENERATE_ACCESS_TOKEN",
            email=user.email,
            level="SUCCESS",
            session_id=session_id,
        )

    @classmethod
    def generate_business_secret_key(cls, user, session_id):
        business = BusinessService.get_business(user=user)
        token_data = TokenManager.prepare_user_token(user, session_id)
        encrypted_access_token = EncryptionClass.encrypt_data(token_data["access"])
        access_token_string = base64.b64encode(encrypted_access_token).decode()
        business.e_secret_key = access_token_string
        business.save()
        return True


class BusinessService:
    @classmethod
    def create_business(cls, user, **kwargs):
        business = Business.objects.create(user=user, **kwargs)
        return business

    @classmethod
    def get_business(cls, **kwargs) -> Business:
        """Get a business instance"""
        return Business.objects.filter(**kwargs).first()

    @classmethod
    def update_webhook(cls, user, data, session_id):
        business = cls.get_business(user=user)
        business.webhook_url = data.get("webhook_url")
        business.save()
        track_user_activity(
            context={},
            category="BUSINESS_ACCOUNT",
            action="BUSINESS_UPDATE_WEBHOOK_URL",
            email=user.email,
            level="SUCCESS",
            session_id=session_id,
        )

    @classmethod
    def initiate_transaction(cls, user, amount, session_id, callback_url):
        from wallet.service import TransactionService

        transaction_obj = TransactionService.get_transaction(
            user=user,
            amount=Decimal(amount),
            transaction_type="CREDIT",
            transaction_status="PENDING",
            pssp="PAYSTACK",
        ).first()
        if transaction_obj:
            authorization_url = transaction_obj.pssp_meta_data["authorization_url"]
            return authorization_url

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
            action="BUSINESS_INITIATE_CARD_TRANSACTION",
            email=user.email,
            level="SUCCESS",
            session_id=session_id,
        )
        return authorization_url

    @classmethod
    def get_business_user_secret_key(cls, user):
        business = BusinessService.get_business(user=user)
        if business.e_secret_key is None:
            return None
        encrypted_access_token = base64.b64decode(business.e_secret_key)
        return EncryptionClass.decrypt_data(encrypted_access_token)
