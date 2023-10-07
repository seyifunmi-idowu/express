from django.db import transaction

from authentication.service import AuthService, UserService
from authentication.tasks import track_user_activity
from helpers.db_helpers import select_for_update
from rider.models import Rider
from rider.serializers import RetrieveRiderSerializer


class RiderService:
    @classmethod
    def create_rider(cls, user, vehicle_type, **kwargs):
        rider = Rider.objects.create(user=user, vehicle_type=vehicle_type, **kwargs)
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
        vehicle_type = kwargs.get("vehicle_type")
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
            )
            cls.create_rider(user=instance_user, vehicle_type=vehicle_type)

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

        return True

    @classmethod
    def rider_login(cls, session_id, **kwargs):
        email = kwargs.get("email")
        phone = kwargs.get("phone")
        password = kwargs.get("password")

        login_token = AuthService.login_user(
            email=email,
            phone_number=phone,
            password=password,
            session_id=session_id,
            login_user_type="RIDER",
        )
        user = UserService.get_user_instance(email=email)
        rider = cls.get_rider(user=user)

        return {"rider": RetrieveRiderSerializer(rider).data, "token": login_token}

    @classmethod
    def upload_document(cls, user, session_id, **kwargs):
        pass
