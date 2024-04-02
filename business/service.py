import base64

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
    def get_business_user_secret_key(cls, user):
        business = BusinessService.get_business(user=user)
        if business.e_secret_key is None:
            return None
        encrypted_access_token = base64.b64decode(business.e_secret_key)
        return EncryptionClass.decrypt_data(encrypted_access_token)
