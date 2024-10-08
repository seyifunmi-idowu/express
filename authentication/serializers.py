from rest_framework import serializers

from authentication.models import User
from helpers.validators import FieldValidators


class UserProfileSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField("get_display_name")
    is_rider = serializers.SerializerMethodField("get_is_rider")
    is_customer = serializers.SerializerMethodField("get_is_customer")
    wallet_balance = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "email_verified",
            "phone_number",
            "phone_verified",
            "avatar_url",
            "street_address",
            "city",
            "last_login",
            "referral_code",
            "is_rider",
            "is_customer",
            "display_name",
            "wallet_balance",
        )

    def get_is_rider(self, obj):
        return obj.user_type == "RIDER"

    def get_is_customer(self, obj):
        return obj.user_type == "CUSTOMER"

    def get_display_name(self, obj):
        return obj.display_name

    def get_wallet_balance(self, obj):
        return obj.get_user_wallet().balance

    def get_avatar_url(self, obj):
        if obj.user_type == "RIDER":
            from rider.service import RiderService

            return RiderService.get_rider(user=obj).photo_url()
        return obj.avatar_url


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[FieldValidators.validate_existing_user_email]
    )


class VerifyForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[FieldValidators.validate_existing_user_email]
    )
    password = serializers.CharField(validators=[FieldValidators.validate_password])
    verify_password = serializers.CharField()
    otp = serializers.CharField()

    def validate(self, data):
        password = data.get("password")
        verify_password = data.get("verify_password")
        if password != verify_password:
            raise serializers.ValidationError("Passwords do not match.")

        return data


class CustomizeReferralCodeSerializer(serializers.Serializer):
    referral_code = serializers.CharField(max_length=30)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password = serializers.CharField(validators=[FieldValidators.validate_password])
    verify_password = serializers.CharField()

    def validate(self, data):
        password = data.get("password")
        verify_password = data.get("verify_password")
        old_password = data.get("old_password")
        if password != verify_password:
            raise serializers.ValidationError("Passwords do not match.")

        if old_password == password:
            raise serializers.ValidationError(
                "New password cannot be the same as old password"
            )

        return data
