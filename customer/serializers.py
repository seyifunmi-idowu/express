from rest_framework import serializers

from authentication.serializers import UserProfileSerializer
from customer.models import Customer
from helpers.validators import FieldValidators
from order.models import Address


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
    referral_code = serializers.CharField(required=False, default="")

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

        if errors:
            raise serializers.ValidationError(errors)

        return data


class CompleteBusinessCustomerSignupSerializer(serializers.Serializer):
    session_token = serializers.CharField(required=True)
    business_name = serializers.CharField(required=True)
    business_address = serializers.CharField(required=True)
    business_category = serializers.CharField(required=True)
    delivery_volume = serializers.IntegerField(required=True)


class ResendCustomerVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[FieldValidators.validate_existing_user_email], required=False
    )
    phone_number = serializers.CharField(
        min_length=10,
        max_length=15,
        validators=[
            FieldValidators.validate_phone_number,
            FieldValidators.validate_existing_user_phone,
        ],
        required=False,
    )

    def validate(self, data):
        FieldValidators.validate_email_or_phone_number(data)
        return data


class RetrieveCustomerSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    business_profile_updated = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ("id", "user", "customer_type", "business_profile_updated")

    def get_business_profile_updated(self, obj):
        return obj.customer_type == "BUSINESS" and obj.business_name is not None


class CompleteAuthBusinessCustomerSignupSerializer(serializers.Serializer):
    business_name = serializers.CharField(required=True)
    business_address = serializers.CharField(required=False)
    business_category = serializers.CharField(required=False)
    delivery_volume = serializers.IntegerField(required=False)


class UpdateCustomerProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(
        validators=[FieldValidators.validate_non_existing_user_email], required=False
    )
    phone_number = serializers.CharField(
        min_length=10,
        max_length=15,
        validators=[
            FieldValidators.validate_phone_number,
            FieldValidators.validate_non_existing_user_phone,
        ],
        required=False,
    )
    avatar = serializers.FileField(write_only=True, required=False)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "id",
            "formatted_address",
            "longitude",
            "latitude",
            "landmark",
            "direction",
        )


class UpdateAddressSerializer(serializers.Serializer):
    formatted_address = serializers.CharField(required=False)
    landmark = serializers.CharField(required=False)
    direction = serializers.CharField(required=False)
    label = serializers.CharField(required=False)


class CreateAddressSerializer(UpdateAddressSerializer):
    latitude = serializers.CharField(max_length=50)
    longitude = serializers.CharField(max_length=50)
