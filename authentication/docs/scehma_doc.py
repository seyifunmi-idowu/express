from drf_yasg import openapi

UNAUTHENTICATED = {
    "application/json": {"message": "Token is invalid or expired"}  # type: ignore
}
NOT_FOUND = {"application/json": {"message": "Object not found."}}

OTP_SUCCESS_RESPONSE = {
    "application/json": {"data": {}, "message": "Verification successful"}
}
EXPIRE_RESPONSE = {"application/json": {"message": "Oops seems the link has expired."}}

VERIFY_OTP_RESPONSES = {
    201: openapi.Response(
        description="Verification successful", examples=OTP_SUCCESS_RESPONSE
    ),
    400: openapi.Response(description="Bad Input", examples=EXPIRE_RESPONSE),
}


USER_DATA_EXAMPLE = {
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
    "display_name": "John Mark",
}
USER_DATA = {"application/json": {"data": USER_DATA_EXAMPLE, "message": ""}}
GET_USER_DATA = {
    200: openapi.Response(
        description="retrieved user data successfully", examples=USER_DATA
    ),
    403: openapi.Response(description="Unauthorized", examples=UNAUTHENTICATED),
}
NO_DATA = {"application/json": {"data": {}, "message": ""}}
LOGOUT_RESPONSE = {
    200: openapi.Response(description="logout successfully", examples=NO_DATA),
    403: openapi.Response(description="Unauthorized", examples=UNAUTHENTICATED),
}
FORGOT_PASSWORD_WRONG_EMAIL = {
    "application/json": {
        "errors": {"email": ["User with email address not found"]},
        "message": "",
    }
}
FORGOT_PASSWORD_RESPONSE = {
    200: openapi.Response(
        description="OTP sent",
        examples={"application/json": {"data": {}, "message": "OTP sent"}},
    ),
    400: openapi.Response(
        description="Bad request", examples=FORGOT_PASSWORD_WRONG_EMAIL
    ),
}
FORGOT_PASSWORD_WRONG_OTP = {
    "application/json": {
        "errors": {"code": ["Oops seems you have an invalid verification code."]},
        "message": "",
    }
}
VERIFY_FORGOT_PASSWORD_RESPONSE = {
    200: openapi.Response(
        description="OTP sent",
        examples={
            "application/json": {"data": {}, "message": "Password reset successful"}
        },
    ),
    400: openapi.Response(
        description="Bad request", examples=FORGOT_PASSWORD_WRONG_OTP
    ),
}
