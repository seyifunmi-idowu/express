from django.db import transaction
from rest_framework import status

from authentication.service import AuthService, UserService
from authentication.tasks import track_user_activity
from helpers.db_helpers import select_for_update
from helpers.exceptions import CustomAPIException
from helpers.s3_uploader import S3Uploader
from notification.service import EmailManager
from rider.models import Rider, RiderDocument
from rider.serializers import (
    RetrieveKycSerializer,
    RetrieveRiderSerializer,
    VehicleInformationSerializer,
)


class RiderService:
    @classmethod
    def create_rider(cls, user, **kwargs):
        rider = Rider.objects.create(user=user, **kwargs)
        return rider

    @classmethod
    def get_rider(cls, **kwargs) -> Rider:
        """Get a rider instance"""
        return Rider.objects.filter(**kwargs).first()

    @classmethod
    def get_and_lock_rider(cls, **kwargs):
        """
        Get rider and lock down that rider instance until the
        transaction is complete. This method should only be
        called in an atomic block
        """
        return select_for_update(Rider, **kwargs)

    @classmethod
    def list_riders(cls, **kwargs):
        """List riders"""
        return Rider.objects.filter(**kwargs)

    @classmethod
    def update_rider(cls, rider: Rider, **kwargs) -> Rider:
        """A service method that updates a Rider's data"""
        for field, value in kwargs.items():
            setattr(rider, field, value)
        rider.save(update_fields=kwargs.keys())
        return rider

    @classmethod
    def register_rider(cls, session_id, **kwargs):
        """
        A service method that creates a rider profile
        :param session_id: used to track user activity
        :param kwargs:
        :return:
        """
        email = kwargs.get("email")
        phone_number = kwargs.get("phone_number")
        fullname = kwargs.get("fullname")
        password = kwargs.get("password")
        one_signal_id = kwargs.get("one_signal_id")
        first_name = fullname.split(" ")[0]
        last_name = fullname.split(" ")[1]

        with transaction.atomic():
            instance_user = UserService.create_user(
                email=email,
                phone_number=phone_number,
                user_type="RIDER",
                first_name=first_name,
                last_name=last_name,
                password=password,
                one_signal_id=one_signal_id,
            )
            cls.create_rider(user=instance_user)

            # AuthService.initiate_email_verification(email=email, name=fullname)
            AuthService.initiate_phone_verification(phone_number)

            track_user_activity(
                context={"full_name": fullname},
                category="RIDER_AUTH",
                action="RIDER_SIGNUP",
                email=email,
                level="SUCCESS",
                session_id=session_id,
            )
            email_manager = EmailManager(
                "Welcome",
                context={"display_name": instance_user.display_name},
                template="rider_signup.html",
            )
            email_manager.send([instance_user.email])

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
            category="RIDER_AUTH",
            action="RIDER_RESEND_OTP",
            email=email,
            level="SUCCESS",
            session_id=session_id,
        )
        return True

    @classmethod
    def rider_login(cls, session_id, **kwargs):
        email = kwargs.get("email")
        phone = kwargs.get("phone")
        password = kwargs.get("password")

        login_token = AuthService.login_user(
            email=email, phone_number=phone, password=password, session_id=session_id
        )
        user = UserService.get_user_instance(email=email)
        rider = cls.get_rider(user=user)

        return {**RetrieveRiderSerializer(rider).data, "token": login_token}

    @classmethod
    def update_rider_vehicle(cls, user, session_id, **kwargs):
        with transaction.atomic():
            rider = cls.get_rider(user=user)
            rider.vehicle_type = kwargs.get("vehicle_type", rider.vehicle_type)
            rider.vehicle_make = kwargs.get("vehicle_make", rider.vehicle_make)
            rider.vehicle_model = kwargs.get("vehicle_model", rider.vehicle_model)
            rider.vehicle_plate_number = kwargs.get(
                "vehicle_plate_number", rider.vehicle_plate_number
            )
            rider.vehicle_color = kwargs.get("vehicle_color", rider.vehicle_color)
            rider.save()
            track_user_activity(
                context=kwargs,
                category="RIDER_KYC",
                action="RIDER_UPDATE_VEHICLE",
                email=user.email if user.email else None,
                phone_number=user.phone_number if user.phone_number else None,
                level="SUCCESS",
                session_id=session_id,
            )
            return VehicleInformationSerializer(rider).data

    @classmethod
    def set_rider_avatar_with_passport(cls, rider):
        if rider.status == "APPROVED" and rider.avatar_url is None:
            rider.avatar_url = rider.photo_url()
            rider.save()
        return True


class RiderKYCService:
    @classmethod
    def get_rider_document(cls, rider, **kwargs):
        return RiderDocument.objects.filter(rider=rider, **kwargs)

    @classmethod
    def get_rider_document_status(cls, rider, document_type):
        documents = cls.get_rider_document(rider=rider, type=document_type)
        if len(documents) < 1:
            return {"status": "unverified", "files": []}

        all_verified = all(photo.verified for photo in documents)
        file_urls = [photo.file_url for photo in documents]
        return {
            "status": "verified" if all_verified else "unverified",
            "files": file_urls,
        }

    @classmethod
    def submit_kyc(cls, user, session_id, **kwargs):
        from order.service import VehicleService

        vehicle_id = kwargs.pop("vehicle_id")
        vehicle = VehicleService.get_vehicle(vehicle_id)
        if vehicle.status != "ACTIVE":
            raise CustomAPIException(
                "vehicle is not active for order", status.HTTP_400_BAD_REQUEST
            )

        rider = RiderService.get_rider(user=user)
        rider.vehicle_color = kwargs.pop("vehicle_color", None)
        rider.vehicle_plate_number = kwargs.pop("vehicle_plate_number", None)
        rider.vehicle = vehicle
        rider.save()

        for field_name, files in kwargs.items():
            for file in files:
                cls.add_rider_document(
                    rider=rider,
                    document_type=field_name,
                    file=file,
                    session_id=session_id,
                )

        rider.save()
        track_user_activity(
            context={},
            category="RIDER_KYC",
            action="RIDER_SUBMIT_KYC",
            email=user.email if user.email else None,
            phone_number=user.phone_number if user.phone_number else None,
            level="SUCCESS",
            session_id=session_id,
        )

        return RetrieveKycSerializer(rider).data

    @classmethod
    def add_rider_document(cls, rider, document_type, file, session_id=None, **kwargs):
        file_name = file.name
        file_url = S3Uploader(
            append_folder=f"/rider_document/{document_type}"
        ).upload_file_object(file, file_name)

        rider_document = RiderDocument.objects.create(
            rider=rider, type=document_type, file_url=file_url, **kwargs
        )
        track_user_activity(
            context={"file_name": file_name, "rider_document": rider_document.id},
            category="RIDER_KYC",
            action="RIDER_ADD_DOCUMENT",
            email=rider.user.email if rider.user.email else None,
            phone_number=rider.user.phone_number if rider.user.phone_number else None,
            level="SUCCESS",
            session_id=session_id,
        )
        return rider_document
