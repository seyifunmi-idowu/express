from rest_framework import serializers, status

from authentication.serializers import UserProfileSerializer
from helpers.validators import FieldValidators
from rider.models import Rider


class RiderSignupSerializer(serializers.Serializer):
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
    address = serializers.CharField()
    VEHICLE_TYPE_CHOICES = [
        ("BICYCLE", "BICYCLE"),
        ("CAR", "CAR (SEDAN)"),
        ("KEKE", "KEKE"),
        ("MOTORCYCLE", "MOTORCYCLE"),
        ("MPV", "MPV (MULTI-PURPOSE VAN)"),
        ("TRUCKS", "TRUCKS"),
    ]
    CITY_CHOICES = [("MAKURDI", "MAKURDI"), ("GBOKO", "GBOKO"), ("OTUKPO", "OTUKPO")]
    vehicle_type = serializers.ChoiceField(choices=VEHICLE_TYPE_CHOICES)
    city = serializers.ChoiceField(choices=CITY_CHOICES)
    password = serializers.CharField(validators=[FieldValidators.validate_password])
    verify_password = serializers.CharField()

    def validate(self, data):
        fullname = data.get("fullname")
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


class VerifyOtpSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    email = serializers.EmailField(
        required=False, validators=[FieldValidators.validate_existing_user_email]
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


class RiderLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    password = serializers.CharField()

    def validate(self, data):
        FieldValidators.validate_email_or_phone_number(data)
        return data


class RetrieveRiderSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Rider
        fields = (
            "id",
            "user",
            "status",
            "vehicle_type",
            "vehicle_make",
            "vehicle_model",
            "vehicle_plate_number",
            "vehicle_color",
            "rider_info",
            "city",
            "avatar_url",
            "vehicle_photos",
        )


class DocumentUploadSerializer(serializers.ModelSerializer):
    vehicle_photos = serializers.ListField(
        child=serializers.ImageField(),
        allow_empty_file=False,
        write_only=True,
    )
