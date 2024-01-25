from drf_yasg import openapi

CUSTOMER_INFO = {
    "id": "1f1d831988564d0eb6adcf6a5bbcb0a0",
    "user": {
        "id": "3979c56f95d4474580f466b7123e955f",
        "first_name": "John",
        "last_name": "Mark",
        "email": "johnmark@yahoo.com",
        "email_verified": False,
        "phone_number": "+2348105474517",
        "phone_verified": True,
        "street_address": None,
        "city": None,
        "last_login": "2023-10-04T07:17:48.924120Z",
        "is_rider": False,
        "is_customer": True,
        "display_name": "John Mark",
        "wallet_balance": 1000.0,
    },
    "status": "UNAPPROVED",
    "vehicle_type": "CAR",
}
UNAUTHENTICATED = {
    "application/json": {"message": "Token is invalid or expired"}  # type: ignore
}
NOT_FOUND = {"application/json": {"message": "Object not found."}}

REGISTRATION_SUCCESS_RESPONSE = {
    "application/json": {
        "data": {"session_token": "SESSION-d8e1cf97ba8440119e368636fae3eca2"},
        "message": "Customer sign up successful",
    }
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

CUSTOMER_REGISTRATION_RESPONSES = {
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
REGISTRATION_SUCCESS_RESPONSE = {
    "application/json": {"data": {}, "message": "Customer sign up successful"}
}
INVALID_SESSION_TOKEN_RESPONSE = {
    "application/json": {"message": "Invalid session token."}
}
MISSING_INPUT_RESPONSE = {
    "application/json": {"errors": {"session_token": ["This field is required."]}}
}

COMPLETE_BUSINESS_CUSTOMER_REGISTRATION_RESPONSES = {
    201: openapi.Response(
        description="Created User", examples=REGISTRATION_SUCCESS_RESPONSE
    ),
    400: openapi.Response(description="Bad Input", examples=MISSING_INPUT_RESPONSE),
    401: openapi.Response(
        description="Invalid session id", examples=INVALID_SESSION_TOKEN_RESPONSE
    ),
}

LOGIN_SUCCESS_RESPONSE = {
    "application/json": {
        "data": {
            "customer": CUSTOMER_INFO,
            "token": {
                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9....",
                "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9....",
            },
        }
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
CUSTOMER_INFO_SUCCESS_RESPONSE = {
    "application/json": {"data": CUSTOMER_INFO, "message": "Customer info"}
}
CUSTOMER_INFO_RESPONSE = {
    200: openapi.Response(
        description="Customer information", examples=CUSTOMER_INFO_SUCCESS_RESPONSE
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
}
OTP_RESENT_SUCCESS_RESPONSE = {"application/json": {"data": {}, "message": "Otp sent"}}
EMAIL_REGISTRATION_NONE_EXISITING_USER_RESPONSE = {
    "application/json": {"errors": {"email": ["User with email address not found"]}}
}
CUSTOMER_RESEND_OTP_RESPONSES = {
    201: openapi.Response(description="Otp sent", examples=OTP_RESENT_SUCCESS_RESPONSE),
    400: openapi.Response(
        description="Bad Input", examples=EMAIL_REGISTRATION_BAD_INPUT_RESPONSE
    ),
    409: openapi.Response(
        description="Existing User",
        examples=EMAIL_REGISTRATION_NONE_EXISITING_USER_RESPONSE,
    ),
}
