from drf_yasg import openapi

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
