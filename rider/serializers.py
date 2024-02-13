from datetime import timedelta

from django.db.models import Sum
from django.utils import timezone
from rest_framework import serializers

from authentication.serializers import UserProfileSerializer
from helpers.validators import FieldValidators
from rider.models import FavoriteRider, Rider, RiderRating


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
    one_signal_id = serializers.CharField(required=False)

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


class ResendVerificationSerializer(serializers.Serializer):
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


class RiderHomepageSerializerSerializer(serializers.ModelSerializer):
    total_deliveries = serializers.SerializerMethodField()
    ongoing_deliveries = serializers.SerializerMethodField()
    delivery_request = serializers.SerializerMethodField()
    today_earns = serializers.SerializerMethodField()
    this_week_earns = serializers.SerializerMethodField()
    rider_activity = serializers.SerializerMethodField()

    class Meta:
        model = Rider
        fields = (
            "id",
            "total_deliveries",
            "ongoing_deliveries",
            "delivery_request",
            "today_earns",
            "this_week_earns",
            "rider_activity",
        )

    def get_total_deliveries(self, obj):
        from order.service import OrderService

        return OrderService.get_order_qs(
            rider=obj, status__in=["ORDER_DELIVERED", "ORDER_COMPLETED"]
        ).count()

    def get_delivery_request(self, obj):
        from order.service import OrderService

        return OrderService.get_order_qs(
            rider=obj, status="PENDING_RIDER_CONFIRMATION"
        ).count()

    def get_ongoing_deliveries(self, obj):
        from order.service import OrderService

        return OrderService.get_order_qs(
            rider=obj,
            status__in=[
                "RIDER_ACCEPTED_ORDER",
                "RIDER_AT_PICK_UP",
                "RIDER_PICKED_UP_ORDER",
                "ORDER_ARRIVED",
            ],
        ).count()

    def get_today_earns(self, obj):
        from order.service import OrderService

        today = timezone.now().date()
        today_earnings = OrderService.get_order_qs(
            rider=obj, created_at__date=today
        ).aggregate(Sum("total_amount"))["total_amount__sum"]
        return today_earnings or 0.0

    def get_this_week_earns(self, obj):
        from order.service import OrderService

        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        this_week_earnings = OrderService.get_order_qs(
            rider=obj, created_at__date__range=[start_of_week, today]
        ).aggregate(Sum("total_amount"))["total_amount__sum"]
        return this_week_earnings or 0.0

    def get_rider_activity(self, obj):
        from wallet.serializers import GetTransactionsSerializer
        from wallet.service import TransactionService

        transactions = TransactionService.get_user_transaction(obj.user).order_by(
            "-created_at"
        )[:10]
        serializer = GetTransactionsSerializer(transactions, many=True)
        return serializer.data


class RetrieveRiderSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    status = serializers.SerializerMethodField()
    vehicle_photos = serializers.SerializerMethodField()
    vehicle = serializers.SerializerMethodField()
    total_orders = serializers.SerializerMethodField()
    total_earns = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Rider
        fields = (
            "id",
            "user",
            "status",
            "vehicle",
            "vehicle_make",
            "vehicle_model",
            "vehicle_plate_number",
            "vehicle_color",
            "rider_info",
            "city",
            "avatar_url",
            "vehicle_photos",
            "total_orders",
            "total_earns",
            "review_count",
        )

    def get_vehicle_photos(self, obj):
        return obj.vehicle_photos()

    def get_vehicle(self, obj):
        return obj.vehicle.name if obj.vehicle else None

    def get_status(self, obj):
        return obj.get_rider_status()

    def get_total_orders(self, obj):
        from order.service import OrderService

        return (
            OrderService.get_order_qs(rider=obj)
            .exclude(status__in=["PROCESSING_ORDER", "PENDING", "ORDER_CANCELLED"])
            .count()
        )

    def get_total_earns(self, obj):
        from order.service import OrderService

        orders = OrderService.get_order_qs(rider=obj, status__in=["ORDER_COMPLETED"])
        total_amount_sum = (
            orders.aggregate(Sum("total_amount"))["total_amount__sum"] or 0.0
        )
        fele_amount_sum = (
            orders.aggregate(Sum("fele_amount"))["fele_amount__sum"] or 0.0
        )
        total_earns = float(total_amount_sum) - float(fele_amount_sum)
        return total_earns

    def get_review_count(self, obj):
        return RiderRating.objects.filter(rider=obj).count()


class DocumentUploadSerializer(serializers.Serializer):
    DOCUMENT_TYPE_CHOICES = [
        ("vehicle_photo", "vehicle_photo"),
        ("passport_photo", "passport_photo"),
        ("government_id", "government_id"),
        ("guarantor_letter", "guarantor_letter"),
        ("address_verification", "address_verification"),
        ("driver_license", "driver_license"),
        ("insurance_certificate", "insurance_certificate"),
        ("certificate_of_vehicle_registration", "certificate_of_vehicle_registration"),
        ("authorization_letter", "authorization_letter"),
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
    vehicle_id = serializers.CharField()
    vehicle_plate_number = serializers.CharField(max_length=20, required=False)
    vehicle_color = serializers.CharField(max_length=20, required=False)
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
    driver_license = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    insurance_certificate = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    certificate_of_vehicle_registration = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    authorization_letter = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )

    class Meta:
        fields = [
            "vehicle_id",
            "vehicle_plate_number",
            "vehicle_color",
            "vehicle_photo",
            "passport_photo",
            "government_id",
            "guarantor_letter",
            "address_verification",
            "driver_license",
            "insurance_certificate",
            "certificate_of_vehicle_registration",
            "authorization_letter",
        ]


class RetrieveKycSerializer(serializers.Serializer):
    status = serializers.SerializerMethodField()
    vehicle_photo = serializers.SerializerMethodField()
    passport_photo = serializers.SerializerMethodField()
    government_id = serializers.SerializerMethodField()
    guarantor_letter = serializers.SerializerMethodField()
    address_verification = serializers.SerializerMethodField()
    driver_license = serializers.SerializerMethodField()
    insurance_certificate = serializers.SerializerMethodField()
    certificate_of_vehicle_registration = serializers.SerializerMethodField()
    authorization_letter = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.get_rider_status()

    def get_vehicle_photo(self, obj):
        from rider.service import RiderKYCService

        return RiderKYCService.get_rider_document_status(obj, "vehicle_photo")

    def get_passport_photo(self, obj):
        from rider.service import RiderKYCService

        return RiderKYCService.get_rider_document_status(obj, "passport_photo")

    def get_government_id(self, obj):
        from rider.service import RiderKYCService

        return RiderKYCService.get_rider_document_status(obj, "government_id")

    def get_guarantor_letter(self, obj):
        from rider.service import RiderKYCService

        return RiderKYCService.get_rider_document_status(obj, "guarantor_letter")

    def get_address_verification(self, obj):
        from rider.service import RiderKYCService

        return RiderKYCService.get_rider_document_status(obj, "address_verification")

    def get_driver_license(self, obj):
        from rider.service import RiderKYCService

        return RiderKYCService.get_rider_document_status(obj, "driver_license")

    def get_insurance_certificate(self, obj):
        from rider.service import RiderKYCService

        return RiderKYCService.get_rider_document_status(obj, "insurance_certificate")

    def get_certificate_of_vehicle_registration(self, obj):
        from rider.service import RiderKYCService

        return RiderKYCService.get_rider_document_status(
            obj, "certificate_of_vehicle_registration"
        )

    def get_authorization_letter(self, obj):
        from rider.service import RiderKYCService

        return RiderKYCService.get_rider_document_status(obj, "authorization_letter")


class VehicleInformationSerializer(serializers.Serializer):
    vehicle = serializers.SerializerMethodField()
    vehicle_make = serializers.SerializerMethodField()
    vehicle_model = serializers.SerializerMethodField()
    vehicle_plate_number = serializers.SerializerMethodField()
    vehicle_color = serializers.SerializerMethodField()
    driver_license = serializers.SerializerMethodField()
    insurance_certificate = serializers.SerializerMethodField()

    def get_vehicle(self, obj):
        return obj.vehicle.name if obj.vehicle else None

    def get_vehicle_make(self, obj):
        return obj.vehicle_make

    def get_vehicle_model(self, obj):
        return obj.vehicle_model

    def get_vehicle_plate_number(self, obj):
        return obj.vehicle_plate_number

    def get_vehicle_color(self, obj):
        return obj.vehicle_color

    def get_driver_license(self, obj):
        from rider.service import RiderKYCService

        return RiderKYCService.get_rider_document_status(obj, "driver_license")

    def get_insurance_certificate(self, obj):
        from rider.service import RiderKYCService

        return RiderKYCService.get_rider_document_status(obj, "insurance_certificate")


class UpdateVehicleSerializer(serializers.ModelSerializer):
    vehicle_make = serializers.CharField(max_length=30, required=False)
    vehicle_model = serializers.CharField(max_length=30, required=False)
    vehicle_plate_number = serializers.CharField(max_length=30, required=False)
    vehicle_color = serializers.CharField(max_length=30, required=False)

    class Meta:
        model = Rider
        fields = (
            "vehicle_make",
            "vehicle_model",
            "vehicle_plate_number",
            "vehicle_color",
        )


class FavouriteRiderSerializer(serializers.ModelSerializer):
    rider = serializers.SerializerMethodField()

    class Meta:
        model = FavoriteRider
        fields = ("rider",)

    def get_rider(self, obj):
        return {
            "id": obj.rider.id,
            "display_name": obj.rider.display_name,
            "avatar_url": obj.rider.avatar_url,
            "assigned_orders": obj.rider.get_active_order().count(),
        }
