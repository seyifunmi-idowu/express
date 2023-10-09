from rest_framework import serializers

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
    CITY_CHOICES = [("MAKURDI", "MAKURDI"), ("GBOKO", "GBOKO"), ("OTUKPO", "OTUKPO")]
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
        )


class DocumentUploadSerializer(serializers.Serializer):
    DOCUMENT_TYPE_CHOICES = [
        ("vehicle_photo", "vehicle_photo"),
        ("passport_photo", "passport_photo"),
        ("government_id", "government_id"),
        ("guarantor_letter", "guarantor_letter"),
        ("address_verification", "address_verification"),
    ]
    document_type = serializers.ChoiceField(choices=DOCUMENT_TYPE_CHOICES)
    documents = serializers.ListField(child=serializers.FileField(), write_only=True)


class KycSerializer(serializers.Serializer):
    VEHICLE_TYPE_CHOICES = [
        ("BICYCLE", "BICYCLE"),
        ("CAR", "CAR"),
        ("KEKE", "KEKE"),
        ("MOTORCYCLE", "MOTORCYCLE"),
        ("MPV", "MPV"),
        ("TRUCKS", "TRUCKS"),
    ]
    vehicle_type = serializers.ChoiceField(choices=VEHICLE_TYPE_CHOICES)
    vehicle_plate_number = serializers.CharField(max_length=20)
    vehicle_color = serializers.CharField(max_length=20)
    vehicle_photo = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    passport_photo = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    government_id = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    guarantor_letter = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    address_verification = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )

    class Meta:
        fields = [
            "vehicle_type",
            "vehicle_plate_number",
            "vehicle_color",
            "vehicle_photo",
            "passport_photo",
            "government_id",
            "guarantor_letter",
            "address_verification",
        ]
