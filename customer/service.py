from django.db import transaction

from authentication.service import AuthService, UserService
from authentication.tasks import track_user_activity
from customer.models import Customer
from customer.serializers import RetrieveCustomerSerializer
from helpers.db_helpers import select_for_update


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
        email = kwargs.get("email")
        phone_number = kwargs.get("phone_number")
        fullname = kwargs.get("fullname")
        password = kwargs.get("password")
        receive_email_promotions = kwargs.get("receive_email_promotions")
        customer_type = kwargs.get("customer_type")
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
            )
            cls.create_customer(user=instance_user, customer_type=customer_type)

            # AuthService.initiate_email_verification(email=email, name=fullname)
            AuthService.initiate_phone_verification(phone_number)

            track_user_activity(
                context={"full_name": fullname},
                category="CUSTOMER_AUTH",
                action="CUSTOMER_SIGNUP",
                email=email,
                level="SUCCESS",
                session_id=session_id,
            )

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
