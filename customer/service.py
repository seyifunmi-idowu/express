from django.db import transaction
from rest_framework import status

from authentication.service import AuthService, UserService
from authentication.tasks import track_user_activity
from customer.models import Customer
from customer.serializers import RetrieveCustomerSerializer
from helpers.db_helpers import select_for_update
from helpers.exceptions import CustomAPIException


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
                email=email if email else phone_number,
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
        email = user.email
        phone_number = user.phone_number
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

        business_name = kwargs.get("business_name")
        business_address = kwargs.get("business_address")
        business_category = kwargs.get("business_category")
        delivery_volume = kwargs.get("delivery_volume")

        customer = cls.get_customer(user=user)
        if customer.customer_type != "BUSINESS":
            raise CustomAPIException(
                "User not a business customer.", status.HTTP_401_UNAUTHORIZED
            )
        customer.business_name = business_name
        customer.business_address = business_address
        customer.business_category = business_category
        customer.delivery_volume = delivery_volume
        customer.save()
        track_user_activity(
            context={"business_name": business_name},
            category="CUSTOMER_AUTH",
            action="CUSTOMER_COMPLETE_SIGNUP",
            email=email if email else phone_number,
            level="SUCCESS",
            session_id=session_id,
        )
        return True

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
            email=email,
            level="SUCCESS",
            session_id=session_id,
        )
        return True

    @classmethod
    def customer_login(cls, session_id, **kwargs):
        email = kwargs.get("email")
        phone = kwargs.get("phone")
        password = kwargs.get("password")

        login_token = AuthService.login_user(
            email=email, phone_number=phone, password=password, session_id=session_id
        )
        user = UserService.get_user_instance(email=email)
        customer = cls.get_customer(user=user)

        return {
            "customer": RetrieveCustomerSerializer(customer).data,
            "token": login_token,
        }
