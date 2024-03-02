from django.db import transaction
from rest_framework import status

from authentication.service import AuthService, UserService
from authentication.tasks import track_user_activity
from customer.models import Customer
from customer.serializers import RetrieveCustomerSerializer
from helpers.db_helpers import select_for_update
from helpers.exceptions import CustomAPIException
from order.models import Address


class CustomerService:
    @classmethod
    def create_customer(cls, user, **kwargs):
        rider = Customer.objects.create(user=user, **kwargs)
        return rider

    @classmethod
    def get_customer(cls, **kwargs) -> Customer:
        """Get a customer instance"""
        return Customer.objects.filter(**kwargs).first()

    @classmethod
    def get_and_lock_customer(cls, **kwargs):
        """
        Get customer and lock down that customer instance until the
        transaction is complete. This method should only be
        called in an atomic block
        """
        return select_for_update(Customer, **kwargs)

    @classmethod
    def list_customer(cls, **kwargs):
        """List customers"""
        return Customer.objects.filter(**kwargs)

    @classmethod
    def update_customer(cls, customer: Customer, **kwargs) -> Customer:
        """A service method that updates a Customer's data"""
        for field, value in kwargs.items():
            setattr(customer, field, value)
        customer.save(update_fields=kwargs.keys())
        return customer

    @classmethod
    def update_customer_profile(cls, user, session_id, **kwargs):
        from helpers.s3_uploader import S3Uploader

        email = kwargs.get("email", None)
        first_name = kwargs.get("first_name", None)
        phone_number = kwargs.get("phone_number", None)
        last_name = kwargs.get("last_name", None)

        avatar_file = kwargs.pop("avatar", None)
        if avatar_file:
            file_name = avatar_file.name
            file_url = S3Uploader(
                append_folder=f"/avatar/{user.id}"
            ).upload_file_object(avatar_file, file_name)
            user.avatar_url = file_url

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
            user.email_verified = False
        if phone_number:
            user.phone_number = phone_number
            user.phone_verified = False

        user.save()
        track_user_activity(
            context=dict(**kwargs),
            category="CUSTOMER_AUTH",
            action="CUSTOMER_UPDATE_PROFILE",
            email=user.email if user.email else None,
            phone_number=user.phone_number if user.phone_number else None,
            level="SUCCESS",
            session_id=session_id,
        )
        return user

    @classmethod
    def register_customer(cls, session_id, **kwargs):
        from helpers.cache_manager import CacheManager, KeyBuilder

        email = kwargs.get("email")
        phone_number = kwargs.get("phone_number")
        fullname = kwargs.get("fullname")
        password = kwargs.get("password")
        receive_email_promotions = kwargs.get("receive_email_promotions")
        customer_type = kwargs.get("customer_type")
        business_name = kwargs.get("business_name")
        business_address = kwargs.get("business_address")
        business_category = kwargs.get("business_category")
        delivery_volume = kwargs.get("delivery_volume")
        one_signal_id = kwargs.get("one_signal_id")
        referral_code = kwargs.get("referral_code")
        first_name = fullname.split(" ")[0]
        last_name = fullname.split(" ")[1]

        with transaction.atomic():
            instance_user = UserService.create_user(
                email=email,
                phone_number=phone_number,
                user_type="CUSTOMER",
                first_name=first_name,
                last_name=last_name,
                password=password,
                receive_email_promotions=receive_email_promotions,
                one_signal_id=one_signal_id,
                referral_code=referral_code,
            )
            cls.create_customer(
                user=instance_user,
                customer_type=customer_type,
                business_name=business_name,
                business_address=business_address,
                business_category=business_category,
                delivery_volume=delivery_volume,
            )

            # AuthService.initiate_email_verification(email=email, name=fullname)
            AuthService.initiate_phone_verification(phone_number)

            track_user_activity(
                context={"full_name": fullname},
                category="CUSTOMER_AUTH",
                action="CUSTOMER_SIGNUP",
                email=email if email else None,
                phone_number=phone_number if phone_number else None,
                level="SUCCESS",
                session_id=session_id,
            )
            if customer_type == "BUSINESS":
                key_builder = KeyBuilder.business_user_complete_signup(session_id)
                CacheManager.set_key(
                    key_builder,
                    {"email": email, "phone_number": phone_number},
                    minutes=1440,  # 24 hours * 60 minutes
                )
                return {"session_token": session_id}
            return {}

    @classmethod
    def complete_business_customer_signup(cls, session_id, **kwargs):
        from helpers.cache_manager import CacheManager, KeyBuilder

        session_token = kwargs.get("session_token")
        user = kwargs.get("user", None)
        if user is None:
            key_builder = KeyBuilder.business_user_complete_signup(session_token)
            verification_data = CacheManager.retrieve_key(key_builder)
            if not verification_data:
                raise CustomAPIException(
                    "Invalid session token.", status.HTTP_401_UNAUTHORIZED
                )

            email = verification_data.get("email", None)
            phone_number = verification_data.get("phone_number", None)
            user = UserService.get_user_instance(email=email, phone_number=phone_number)
            CacheManager.delete_key(key_builder)

        email = user.email
        phone_number = user.phone_number

        customer = cls.get_customer(user=user)
        if customer.customer_type != "BUSINESS":
            raise CustomAPIException(
                "User not a business customer.", status.HTTP_401_UNAUTHORIZED
            )
        business_name = kwargs.get("business_name")
        business_address = kwargs.get("business_address")
        business_category = kwargs.get("business_category")
        delivery_volume = kwargs.get("delivery_volume")

        customer.business_name = business_name
        customer.business_address = business_address
        customer.business_category = business_category
        customer.delivery_volume = delivery_volume
        customer.save()
        track_user_activity(
            context={"business_name": business_name},
            category="CUSTOMER_AUTH",
            action="CUSTOMER_COMPLETE_SIGNUP",
            email=email if email else None,
            phone_number=phone_number if phone_number else None,
            level="SUCCESS",
            session_id=session_id,
        )
        return True

    @classmethod
    def change_email_or_phone_number(cls, session_id, **kwargs):
        email = kwargs.get("email", None)
        phone_number = kwargs.get("phone_number", None)
        user = UserService.get_user_instance(email=email, phone_number=phone_number)
        if not user:
            raise CustomAPIException("User not found", status.HTTP_404_NOT_FOUND)

        if email:
            if user.email_verified:
                raise CustomAPIException(
                    "User email already verified", status.HTTP_400_BAD_REQUEST
                )
            context = ({"old_email": user.email, "new_email": phone_number},)
            user.email = email
            AuthService.initiate_email_verification(email=email, name=user.display_name)
        if phone_number:
            if user.phone_verified:
                raise CustomAPIException(
                    "User phone already verified", status.HTTP_400_BAD_REQUEST
                )
            context = (
                {
                    "old_phone_number": user.phone_number,
                    "new_phone_number": phone_number,
                },
            )
            user.phone_number = phone_number
            AuthService.initiate_phone_verification(phone_number)

        track_user_activity(
            context=context,
            category="CUSTOMER_AUTH",
            action="CUSTOMER_CHANGED_PHONE_NUMBER"
            if phone_number
            else "CUSTOMER_CHANGED_EMAIL",
            email=email if email else None,
            phone_number=phone_number if phone_number else None,
            level="SUCCESS",
            session_id=session_id,
        )

    @classmethod
    def resend_verification_code(cls, session_id, **kwargs):
        email = kwargs.get("email", None)
        phone_number = kwargs.get("phone_number", None)
        user = UserService.get_user_instance(email=email, phone_number=phone_number)
        if not user:
            raise CustomAPIException("User not found", status.HTTP_404_NOT_FOUND)

        if email:
            AuthService.initiate_email_verification(email=email, name=user.display_name)
        if phone_number:
            AuthService.initiate_phone_verification(phone_number)

        track_user_activity(
            context={"user": email or phone_number},
            category="CUSTOMER_AUTH",
            action="CUSTOMER_RESEND_OTP",
            email=user.email if user.email else None,
            phone_number=user.phone_number if user.phone_number else None,
            level="SUCCESS",
            session_id=session_id,
        )
        return True

    @classmethod
    def customer_login(cls, session_id, **kwargs):
        email = kwargs.get("email")
        phone = kwargs.get("phone")
        password = kwargs.get("password")
        one_signal_id = kwargs.get("one_signal_id", None)

        login_token = AuthService.login_user(
            email=email,
            phone_number=phone,
            password=password,
            session_id=session_id,
            one_signal_id=one_signal_id,
        )
        user = UserService.get_user_instance(email=email)
        customer = cls.get_customer(user=user)

        return {
            "customer": RetrieveCustomerSerializer(customer).data,
            "token": login_token,
        }

    @classmethod
    def get_customer_favourite_rider(cls, user):
        from rider.models import FavoriteRider

        return FavoriteRider.objects.filter(customer__user=user)


class CustomerAddressService:
    @classmethod
    def create_customer_address(cls, user, **kwargs):
        from order.service import MapService

        customer = CustomerService.get_customer(user=user)
        latitude = kwargs.get("latitude")
        longitude = kwargs.get("longitude")
        direction = kwargs.get("direction", None)
        landmark = kwargs.get("landmark", None)
        label = kwargs.get("label", None)

        address_info = MapService.get_info_from_latitude_and_longitude(
            latitude, longitude
        )
        if len(address_info) < 1:
            raise CustomAPIException(
                "Unable to locate address", status.HTTP_404_NOT_FOUND
            )
        address = Address.objects.create(
            formatted_address=address_info[0].get("formatted_address"),
            customer=customer,
            direction=direction,
            landmark=landmark,
            label=label,
            latitude=address_info[0].get("latitude"),
            longitude=address_info[0].get("longitude"),
        )
        return address

    @classmethod
    def get_customer_address(cls, user):
        return Address.objects.filter(customer__user=user)

    @classmethod
    def delete_customer_address(cls, user, address_id):
        address = Address.objects.filter(id=address_id, customer__user=user).first()
        if not address:
            raise CustomAPIException("Address not found", status.HTTP_404_NOT_FOUND)
        address.delete()
        return True

    @classmethod
    def update_customer_address(cls, user, address_id, **kwargs):
        address = Address.objects.filter(id=address_id, customer__user=user).first()
        if not address:
            raise CustomAPIException("Address not found", status.HTTP_404_NOT_FOUND)

        formatted_address = kwargs.get("formatted_address", address.formatted_address)
        landmark = kwargs.get("landmark", address.landmark)
        direction = kwargs.get("direction", address.direction)
        label = kwargs.get("label", address.label)

        address.formatted_address = formatted_address
        address.direction = direction
        address.landmark = landmark
        address.label = label
        address.save()
        return address
