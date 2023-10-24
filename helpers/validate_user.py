def validate_user(user) -> bool:
    return user.is_authenticated and user.state == "ACTIVE"


def validate_verified_user(user) -> bool:
    return user.email_verified or user.phone_verified


def validate_deactivated_user(request) -> bool:
    from rest_framework import status

    from authentication.models import User
    from helpers.exceptions import CustomAPIException

    user = None
    if "email" in request.data.keys():
        user = User.objects.filter(email=request.data.get("email").lower()).first()
    elif "phone_number" in request.data.keys():
        user = User.objects.filter(
            phone_number=request.data.get("phone_number")
        ).first()
    if user and user.is_deactivated:
        raise CustomAPIException(
            "Your account has been suspended.", status.HTTP_403_FORBIDDEN
        )

    return True


def validate_rider(user) -> bool:
    return user.user_type == "RIDER"


def validate_customer(user) -> bool:
    return user.user_type == "CUSTOMER"


def validate_admin(user) -> bool:
    return user.user_type == "ADMIN"