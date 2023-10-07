from datetime import timedelta

from django.contrib.auth.hashers import check_password
from django.utils import timezone
from rest_framework import status

from authentication.models import User, UserActivity
from authentication.tasks import track_user_activity
from feleexpress import settings
from helpers.cache_manager import CacheManager, KeyBuilder
from helpers.db_helpers import generate_otp
from helpers.exceptions import CustomAPIException, CustomFieldValidationException
from helpers.notification import EmailManager, SMSManager
from helpers.token_manager import TokenManager


class UserService:
    @classmethod
    def create_user(cls, **kwargs):
        user = User.objects.create_user(**kwargs)
        return user

    @classmethod
    def get_user_instance(cls, email=None, phone_number=None, user_id=None):
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                return user
        if phone_number:
            user = User.objects.filter(phone_number=phone_number).first()
            if user:
                return user
        if user_id:
            user = User.objects.filter(pk=user_id).first()
            if user:
                return user

        return None


class AuthService:
    @classmethod
    def initiate_phone_verification(cls, phone_number):
        user = User.objects.filter(phone_number=phone_number).first()
        if user.phone_verified is True:
            raise CustomFieldValidationException(
                "User with this phone number has been verified",
                "phone_numer",
                status.HTTP_400_BAD_REQUEST,
            )

        key_builder = KeyBuilder.user_auth_verification(phone_number)
        trials_count = 1
        tokens = []
        verification_data = CacheManager.retrieve_key(key_builder)
        if verification_data:
            trials_count = verification_data["trials"]
            tokens = verification_data["tokens"]
            if trials_count == settings.PHONE_VERIFICATION_MAX_TRIALS:
                raise CustomAPIException(
                    "Oops you've reached the maximum request for this operation. Retry in 24hrs time.",
                    status.HTTP_429_TOO_MANY_REQUESTS,
                )
            trials_count += 1

        verification_expiry = timezone.now() + timedelta(
            seconds=settings.PHONE_VERIFICATION_TTL
        )
        otp = generate_otp()
        tokens.append({"otp": otp, "expiry": verification_expiry})
        CacheManager.set_key(
            key_builder,
            {"trials": trials_count, "tokens": tokens},
            minutes=1440,  # 24 hours * 60 minutes
        )
        message = f"Your Fele Express OTP is {otp}"

        if settings.ENVIRONMENT == "production":
            # sms will only go out in production environment
            SMSManager().send_message(phone_number, message)
        return True

    @classmethod
    def validate_phone_verification(cls, phone_number, code, session_id):
        key_builder = KeyBuilder.user_auth_verification(phone_number)
        verification_data = CacheManager.retrieve_key(key_builder)
        activity_context = {"phone_number": phone_number, "code": code}
        if not verification_data:
            track_user_activity(
                context=activity_context,
                category="USER_AUTH",
                action="PHONE_VERIFICATION_OTP",
                phone_number=phone_number,
                level="ERROR",
                session_id=session_id,
            )
            raise CustomAPIException(
                "Oops seems the link has expired.", status.HTTP_400_BAD_REQUEST
            )

        tokens = verification_data.get("tokens")
        current_time = timezone.now()
        is_otp_found = False
        for token in tokens:
            if token.get("otp") == code:
                is_otp_found = True
                time_difference_seconds = (
                    current_time - token.get("expiry")
                ).total_seconds()
                if time_difference_seconds > settings.EMAIL_VERIFICATION_TTL:
                    track_user_activity(
                        context=activity_context,
                        category="USER_AUTH",
                        action="PHONE_VERIFICATION_OTP",
                        phone_number=phone_number,
                        level="ERROR",
                        session_id=session_id,
                    )
                    raise CustomAPIException(
                        "Oops seems the link has expired.", status.HTTP_400_BAD_REQUEST
                    )

        if settings.ENVIRONMENT != "production":
            if code == settings.TEST_OTP:
                is_otp_found = True

        if is_otp_found is False:
            track_user_activity(
                context=activity_context,
                category="USER_AUTH",
                action="PHONE_VERIFICATION_OTP",
                phone_number=phone_number,
                level="ERROR",
                session_id=session_id,
            )
            raise CustomFieldValidationException(
                "Oops seems you have an invalid verification code.",
                "code",
                status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(phone_number=phone_number).first()
        if user is None:
            raise CustomFieldValidationException(
                "User with this phone was not found",
                "phone_number",
                status.HTTP_404_NOT_FOUND,
            )
        user.phone_verified = True
        user.save()

        CacheManager.delete_key(key_builder)
        track_user_activity(
            context=activity_context,
            category="USER_AUTH",
            action="PHONE_VERIFICATION_OTP",
            phone_number=phone_number,
            level="SUCCESS",
            session_id=session_id,
        )

        return True

    @classmethod
    def initiate_phone_verification_with_twillio(cls, phone_number):
        SMSManager().send_verification_code(phone_number)

    @classmethod
    def verify_phone_verification_with_twillio(cls, phone_number, code):
        pass

    @classmethod
    def initiate_email_verification(cls, email, name):
        user = User.objects.filter(email=email).first()
        if user.email_verified is True:
            raise CustomFieldValidationException(
                "User with this email address has been verified",
                "email",
                status.HTTP_400_BAD_REQUEST,
            )

        key_builder = KeyBuilder.user_auth_verification(email)
        trials_count = 1
        tokens = []
        verification_data = CacheManager.retrieve_key(key_builder)
        if verification_data:
            trials_count = verification_data["trials"]
            tokens = verification_data["tokens"]
            if trials_count == settings.EMAIL_VERIFICATION_MAX_TRIALS:
                raise CustomAPIException(
                    "Oops you've reached the maximum request for this operation. Retry in 24hrs time.",
                    status.HTTP_429_TOO_MANY_REQUESTS,
                )
            trials_count += 1

        verification_expiry = timezone.now() + timedelta(
            seconds=settings.EMAIL_VERIFICATION_TTL  # email code is valid for 2 hours
        )
        otp = generate_otp()
        tokens.append({"otp": otp, "expiry": verification_expiry})
        CacheManager.set_key(
            key_builder,
            {"trials": trials_count, "tokens": tokens},
            minutes=1440,  # 24 hours * 60 minutes
        )
        email_manager = EmailManager(
            "Verify Email",
            context={"name": name, "otp": otp},
            template="otp_template.html",
        )
        email_manager.send([email])

        return True

    @classmethod
    def validate_email_verification(cls, email, code, session_id):
        key_builder = KeyBuilder.user_auth_verification(email)
        verification_data = CacheManager.retrieve_key(key_builder)
        activity_context = {"email": email, "code": code}
        if not verification_data:
            track_user_activity(
                context=activity_context,
                category="USER_AUTH",
                action="EMAIL_VERIFICATION_OTP",
                email=email,
                level="ERROR",
                session_id=session_id,
            )
            raise CustomAPIException(
                "Oops seems the link has expired.", status.HTTP_400_BAD_REQUEST
            )

        tokens = verification_data.get("tokens")
        current_time = timezone.now()
        is_otp_found = False

        for token in tokens:
            if token.get("otp") == code:
                is_otp_found = True
                time_difference_seconds = (
                    current_time - token.get("expiry")
                ).total_seconds()
                if time_difference_seconds > settings.EMAIL_VERIFICATION_TTL:
                    track_user_activity(
                        context=activity_context,
                        category="USER_AUTH",
                        action="EMAIL_VERIFICATION_OTP",
                        email=email,
                        level="ERROR",
                        session_id=session_id,
                    )
                    raise CustomAPIException(
                        "Oops seems the link has expired.", status.HTTP_400_BAD_REQUEST
                    )

        if is_otp_found is False:
            track_user_activity(
                context=activity_context,
                category="USER_AUTH",
                action="EMAIL_VERIFICATION_OTP",
                email=email,
                level="ERROR",
                session_id=session_id,
            )
            raise CustomFieldValidationException(
                "Oops seems you have an invalid verification code.",
                "code",
                status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(email=email).first()
        if user is None:
            raise CustomFieldValidationException(
                "User with this email was not found", "email", status.HTTP_404_NOT_FOUND
            )
        user.email_verified = True
        user.save()

        CacheManager.delete_key(key_builder)
        track_user_activity(
            context=activity_context,
            category="USER_AUTH",
            action="EMAIL_VERIFICATION_OTP",
            email=email,
            level="SUCCESS",
            session_id=session_id,
        )

        return True

    @classmethod
    def login_user(
        cls,
        session_id: str = None,
        email: str = None,
        phone_number: str = None,
        password: str = None,
        login_user_type="CUSTOMER",
    ):
        if email is not None:
            field_verbose_name = "email"
            user = User.objects.filter(email=email).first()
        else:
            field_verbose_name = "phone number"
            user = User.objects.filter(phone_number=phone_number).first()

        if user is None:
            raise CustomAPIException(
                f"{field_verbose_name.capitalize()} or password is not correct",
                status.HTTP_401_UNAUTHORIZED,
            )

        is_valid_password = check_password(password, user.password)
        if not is_valid_password:
            raise CustomAPIException(
                f"{field_verbose_name.capitalize()} or password is not correct",
                status.HTTP_401_UNAUTHORIZED,
            )

        user.last_login = timezone.now()
        user.last_login_user_type = login_user_type
        user.save()
        return TokenManager.prepare_user_token(user=user, session_id=session_id)


class UserActivityService:
    @classmethod
    def capture_activity(
        cls,
        user,
        context,
        category,
        action,
        rider=None,
        customer=None,
        level="INFO",
        session_id=None,
    ):
        activity = UserActivity(
            user=user,
            rider=rider,
            context=context,
            category=category,
            action=action,
            customer=customer,
            level=level,
            session_id=session_id,
        )
        activity.save()

    @classmethod
    def get_user_activities(cls, request):
        user_id = request.GET.get("user_id")
        categories = request.GET.get("categories")
        level = request.GET.get("level")
        user_types = request.GET.get("user_types")
        user_activity_qs = UserActivity.objects.all().order_by("-created_at")
        if categories:
            categories = categories.split(",")
            user_activity_qs = user_activity_qs.filter(category__in=categories)
        if user_id:
            user_activity_qs = user_activity_qs.filter(user__id=user_id)
        if level:
            level = level.split(",")
            user_activity_qs = user_activity_qs.filter(level__in=level)
        if user_types:
            user_types = user_types.split(",")
            user_activity_qs = user_activity_qs.filter(
                user__user_types__contains=user_types
            )
        return user_activity_qs

    @classmethod
    def retrieve_user_activity_qs(cls, **kwargs):
        """"""
        return UserActivity.objects.filter(**kwargs)
