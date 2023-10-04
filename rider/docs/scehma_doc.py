from drf_yasg import openapi

RIDER_INFO = {
    "id": "1f1d831988564d0eb6adcf6a5bbcb0a0",
    "user": {
        "id": "3979c56f95d4474580f466b7123e955f",
        "first_name": "John",
        "last_name": "Mark",
        "email": "seyiidowu24@yahoo.com",
        "email_verified": False,
        "phone_number": "+2348105474517",
        "phone_verified": True,
        "street_address": None,
        "city": None,
        "last_login": "2023-10-04T07:17:48.924120Z",
        "is_rider": True,
        "is_customer": False,
        "display_name": "John Mark"
    },
    "status": "UNAPPROVED",
    "vehicle_type": "CAR",
    "vehicle_make": None,
    "vehicle_model": None,
    "vehicle_plate_number": None,
    "vehicle_color": None,
    "rider_info": None,
    "city": None,
    "avatar_url": None,
    "vehicle_photos": []
}
UNAUTHENTICATED = {
    "application/json": {"message": "Token is invalid or expired"}  # type: ignore
}
NOT_FOUND = {"application/json": {"message": "Object not found."}}

REGISTRATION_SUCCESS_RESPONSE = {
    "application/json": {"data": {}, "message": "Rider sign up successful"}
}

EMAIL_REGISTRATION_BAD_INPUT_RESPONSE = {
    "application/json": {
        "errors": {
            "email": ["Enter a valid email address."],
            "vehicle_type": ["This field is required."],
        }
    }
}

EMAIL_REGISTRATION_EXISITING_USER_RESPONSE = {
    "application/json": {
        "errors": {"email": ["A user has already registered with this email address"]}
    }
}

RIDER_REGISTRATION_RESPONSES = {
    201: openapi.Response(
        description="Created User", examples=REGISTRATION_SUCCESS_RESPONSE
    ),
    400: openapi.Response(
        description="Bad Input", examples=EMAIL_REGISTRATION_BAD_INPUT_RESPONSE
    ),
    409: openapi.Response(
        description="Existing User", examples=EMAIL_REGISTRATION_EXISITING_USER_RESPONSE
    ),
}

LOGIN_SUCCESS_RESPONSE = {
    "application/json": {
        "data": RIDER_INFO,
        "token": {
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9....",
            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9....",
        },
    },
    "message": "",
}

LOGIN_WITH_EMAIL_UNAUTHORISED_RESPONSE = {
    "application/json": {"message": "Email or password is not correct"}
}

LOGIN_WITH_EMAIL_BAD_INPUT_RESPONSE = {
    "application/json": {
        "errors": {
            "email": ["This field is required."],
            "password": ["This field is required."],
        }
    }
}
LOGIN_RESPONSES = {
    200: openapi.Response(
        description="Successful Login", examples=LOGIN_SUCCESS_RESPONSE
    ),
    400: openapi.Response(
        description="Bad Input", examples=LOGIN_WITH_EMAIL_BAD_INPUT_RESPONSE
    ),
    401: openapi.Response(
        description="Invalid Credentials",
        examples=LOGIN_WITH_EMAIL_UNAUTHORISED_RESPONSE,
    ),
}
RIDER_INFO_SUCCESS_RESPONSE = {
    "application/json": {
        "data": RIDER_INFO,
        "message": "Rider info"
    }
}
RIDER_INFO_RESPONSE = {
    200: openapi.Response(
        description="Rider information", examples=RIDER_INFO_SUCCESS_RESPONSE
    ),
    401: openapi.Response(
        description="Invalid Credentials",
        examples=UNAUTHENTICATED,
    ),
}
