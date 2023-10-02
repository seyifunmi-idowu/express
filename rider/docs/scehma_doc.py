from drf_yasg import openapi

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
        "data": {
            "rider": {
                "id": "1f1d831988564d0eb6adcf6a5bbcb0a0",
                "user": {
                    "id": "3979c56f95d4474580f466b7123e955f",
                    "first_name": "John",
                    "last_name": "Mark",
                    "email": "john@mark.com",
                    "email_verified": False,
                    "phone_number": "+234123456789",
                    "phone_verified": True,
                    "street_address": None,
                    "city": None,
                    "last_login": "2023-10-02T20:43:57.009396Z",
                    "is_rider": True,
                    "is_customer": False,
                    "display_name": "John Mark"
                },
                "vehicle_type": "CAR",
                "rider_info": None,
                "city": None,
                "vehicle_photos": []
            },
        },
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
