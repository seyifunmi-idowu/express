from rest_framework import serializers

from authentication.serializers import UserProfileSerializer
from customer.models import Customer
from helpers.validators import FieldValidators


class CustomerSignupSerializer(serializers.Serializer):
    fullname = serializers.CharField()
    email = serializers.EmailField(
        validators=[FieldValidators.validate_non_existing_user_email]
    )
    phone_number = serializers.CharField(
        min_length=10,
        max_length=15,
        validators=[
            FieldValidators.validate_phone_number,
            FieldValidators.validate_non_existing_user_phone,
        ],
        required=True,
    )
    password = serializers.CharField(validators=[FieldValidators.validate_password])
    verify_password = serializers.CharField()
    receive_email_promotions = serializers.BooleanField(default=False, required=False)
    CUSTOMER_TYPE_CHOICES = [("INDIVIDUAL", "INDIVIDUAL"), ("BUSINESS", "BUSINESS")]
    customer_type = serializers.ChoiceField(choices=CUSTOMER_TYPE_CHOICES)
    one_signal_id = serializers.CharField(required=False)
    business_name = serializers.CharField(required=False)
    business_address = serializers.CharField(required=False)
    business_category = serializers.CharField(required=False)
    delivery_volume = serializers.IntegerField(required=False)

    def validate(self, data):
        errors = {}
        fullname = data.get("fullname")
        if fullname:
            fullname_split = fullname.split()
            if len(fullname_split) < 2:
                errors["fullname"] = "Full name must contain first name and last name."

        password = data.get("password")
        verify_password = data.get("verify_password")
        if password != verify_password:
            errors["password"] = "Passwords do not match."

        customer_type = data.get("customer_type")
        business_name = data.get("business_name")
        business_address = data.get("business_address")
        business_category = data.get("business_category")
        delivery_volume = data.get("delivery_volume")

        if customer_type == "BUSINESS":
            if not business_name:
                errors["business_name"] = "Business name is required for BUSINESS type."
            if not business_address:
                errors[
                    "business_address"
                ] = "Business address is required for BUSINESS type."
            if not business_category:
                errors[
                    "business_category"
                ] = "Business category is required for BUSINESS type."
            if not delivery_volume:
                errors[
                    "delivery_volume"
                ] = "Delivery volume is required for BUSINESS type."

        if errors:
            raise serializers.ValidationError(errors)

        return data


class RetrieveCustomerSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Customer
        fields = ("id", "user", "customer_type")
