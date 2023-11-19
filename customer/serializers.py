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

    def validate(self, data):
        fullname = data.get("fullname")
        if fullname:
            fullname_split = fullname.split()
            if len(fullname_split) != 2:
                raise serializers.ValidationError(
                    "Full name must contain first name and last name."
                )

        password = data.get("password")
        verify_password = data.get("verify_password")
        if password != verify_password:
            raise serializers.ValidationError("Passwords do not match.")

        return data


class RetrieveCustomerSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Customer
        fields = ("id", "user", "customer_type")
